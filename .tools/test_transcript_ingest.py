#!/usr/bin/env python3
"""真相层抽取器与检索的负向/行为测试（v2）。全部用临时目录与合成样例（假密钥），不碰真实记录。
运行：python3 -I ~/Documents/Claude/brain/.tools/test_transcript_ingest.py
"""
import fcntl
import gzip
import importlib.util
import io
import json
import os
import contextlib
import tempfile
import time
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ING = _load("transcript_ingest")
SEA = _load("transcript_search")

# 合成假密钥（拼接构造，均非真实凭证）
FAKE = {
    "anthropic": "sk-ant-" + "api03-" + "A" * 30,
    "sk": "sk-" + "proj-" + "B7" * 15,
    "github": "ghp_" + "C" * 36,
    "aws": "AKIA" + "D" * 16,
    "slack": "xoxb-" + "1234567890-" + "E" * 12,
    "jwt": "eyJ" + "F" * 12 + ".eyJ" + "G" * 12 + "." + "H" * 12,
    "pem": "-----BEGIN RSA PRIVATE KEY-----\nMIIE" + "I" * 40 + "\n-----END RSA PRIVATE KEY-----",
    "bearer": "Authorization: Bearer " + "J" * 24,
    "token": "ts.set_token('" + "a1b2" * 14 + "')",
    "assign": "TUSHARE_TOKEN=" + "k9" * 20,
    "url": "postgres://user:" + "Pa55w0rdX" + "@db.local/x",
    "google": "AIza" + "M" * 35,
}
FAKE_VALUES = ["A" * 30, "B7" * 15, "C" * 36, "D" * 16, "E" * 12, "F" * 12, "I" * 40, "J" * 24,
               "a1b2" * 14, "k9" * 20, "Pa55w0rdX", "M" * 35]
QUOTED_ASSIGN = 'export TUSHARE_TOKEN="' + "q7" * 28 + '"'
EXTRA_TOOL_SECRETS = {
    "quoted": QUOTED_ASSIGN,
    "sk_hex": "ELEVEN_KEY sk_" + "0f" * 24,
    "pro_api": "ts.pro_api('" + "c3d4" * 14 + "')",
    "passwd": "DB_PASSWORD=" + "x@Y!z9#w",
}
EXTRA_VALUES = ["q7" * 28, "0f" * 24, "c3d4" * 14, "x@Y!z9#w"]


def line(obj):
    return json.dumps(obj, ensure_ascii=False) + "\n"


def base_lines(uid_prefix="u"):
    return [
        line({"type": "ai-title", "aiTitle": "测试会话"}),
        line({"type": "user", "uuid": f"{uid_prefix}1", "timestamp": "2026-11-10T01:00:00Z",
              "message": {"role": "user", "content": "请检索 独角兽关键词 并看密钥 " + FAKE["assign"]}}),
        line({"type": "assistant", "uuid": f"{uid_prefix}2", "timestamp": "2026-11-10T01:00:05Z", "message": {"role": "assistant", "content": [
            {"type": "thinking", "thinking": "不应被抽取的思考"},
            {"type": "text", "text": "好的，我来跑命令。"},
            {"type": "tool_use", "id": "tu1", "name": "Bash",
             "input": {"command": " ; ".join(EXTRA_TOOL_SECRETS.values()) + " echo " + FAKE["github"], "big": "Z" * 20000}},
        ]}}),
        line({"type": "user", "uuid": f"{uid_prefix}3", "timestamp": "2026-11-10T01:00:09Z", "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "tu1", "is_error": True,
             "content": [{"type": "text", "text": " ".join(FAKE.values()) + " " + "长" * 3000},
                         {"type": "tool_reference", "tool_name": "WebSearch"}]},
        ]}}),
        "这不是 json\n",
        line({"type": "attachment", "uuid": f"{uid_prefix}4", "timestamp": "2026-11-10T01:00:10Z",
              "attachment": {"type": "queued_command", "commandMode": "prompt", "prompt": "中途插话 白泽之问"}}),
        line({"type": "attachment", "uuid": f"{uid_prefix}5", "timestamp": "2026-11-10T01:00:11Z",
              "attachment": {"type": "queued_command", "commandMode": "prompt", "prompt": "已送达的插话"}}),
        line({"type": "user", "uuid": f"{uid_prefix}6", "timestamp": "2026-11-10T01:00:12Z",
              "message": {"role": "user", "content": "已送达的插话"}}),
        line({"type": "attachment", "uuid": f"{uid_prefix}7", "timestamp": "2026-11-10T01:00:13Z",
              "attachment": {"type": "queued_command", "commandMode": "task-notification", "prompt": "<task-notification>子任务完成 朱雀回报</task-notification>"}}),
    ]


def make_session(path, extra=(), prefix="u"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(base_lines(prefix) + list(extra)), encoding="utf-8")


def read_out(dst):
    files = sorted(Path(dst).rglob("*.jsonl.gz"))
    out = []
    for f in files:
        with gzip.open(f, "rt", encoding="utf-8") as g:
            out.append([json.loads(x) for x in g])
    return files, out


def snapshot(src):
    return {str(p): (p.stat().st_size, p.stat().st_mtime_ns) for p in Path(src).rglob("*") if p.is_file()}


class T(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.src = self.root / "projects"
        self.dst = self.root / "transcripts"
        self.sess = self.src / "-Users-x-proj" / "11111111-aaaa.jsonl"
        make_session(self.sess)
        self.logs = []

    def tearDown(self):
        os.chmod(self.sess, 0o644) if self.sess.exists() else None
        self.tmp.cleanup()

    def ingest(self, sources=None):
        return ING.run(sources or [("code", self.src)], self.dst, log=self.logs.append)

    def recs(self):
        return read_out(self.dst)[1][0][1:]

    # ---- 内容 ----
    def test_c_tier_content_and_header(self):
        self.assertEqual(self.ingest(), 0)
        files, out = read_out(self.dst)
        self.assertEqual(len(files), 1)
        self.assertTrue(files[0].relative_to(self.dst).as_posix().startswith("2026-11/"))
        self.assertIn("_code_11111111-aaaa_", files[0].name)
        h = out[0][0]
        self.assertEqual((h["type"], h["title"], h["session_id"], h["source"], h["project_dir"], h["bad_lines"]),
                         ("header", "测试会话", "11111111-aaaa", "code", "-Users-x-proj", 1))
        self.assertEqual(h["counts"], {"text": 5, "tool_use": 1, "tool_result": 1})
        self.assertNotIn("不应被抽取的思考", json.dumps(out, ensure_ascii=False))
        self.assertTrue(all(r.get("uid") for r in out[0][1:]))
        tr = [r for r in out[0][1:] if r["kind"] == "tool_result"][0]
        self.assertIn("[tool_reference: WebSearch]", tr["text"]) if not tr.get("truncated") else None

    def test_queued_prompt_and_notification(self):
        self.ingest()
        recs = self.recs()
        q = [r for r in recs if r.get("queued")]
        self.assertEqual(sorted(r["text"][:6] for r in q), sorted(["中途插话 白", "<task-"]))
        self.assertEqual([r["role"] for r in q if "白泽" in r["text"]], ["user"])
        self.assertEqual([r["role"] for r in q if "朱雀" in r["text"]], ["notification"])
        self.assertEqual(sum(1 for r in recs if r["text"] == "已送达的插话"), 1, "已送达的插话不得重复")
        self.assertEqual(len(SEA.search(self.dst, "白泽之问", role="user")), 1)

    def test_caps(self):
        self.ingest()
        recs = self.recs()
        tu = [r for r in recs if r["kind"] == "tool_use"][0]
        tr = [r for r in recs if r["kind"] == "tool_result"][0]
        self.assertLessEqual(len(tu["text"].encode()), ING.TOOL_INPUT_CAP)
        self.assertTrue(tu["truncated"])
        self.assertLessEqual(len(tr["text"].encode()), ING.TOOL_RESULT_CAP)
        self.assertTrue(tr["truncated"] and tr["is_error"])

    # ---- 脱敏 ----
    def test_redaction_all_kinds(self):
        self.ingest()
        blob = json.dumps(read_out(self.dst)[1], ensure_ascii=False)
        for v in FAKE_VALUES + EXTRA_VALUES:
            self.assertNotIn(v, blob, f"原值泄漏：{v[:6]}…")
        for k in ["anthropic", "sk", "github", "aws", "slack", "jwt", "pem", "bearer", "token", "assign", "url", "google"]:
            self.assertIn(f"[REDACTED:{k}]", blob, f"{k} 无脱敏标记")

    def test_quoted_assign_inside_tool_use(self):
        self.ingest()
        tu = [r for r in self.recs() if r["kind"] == "tool_use"][0]["text"]
        self.assertIn("TUSHARE_TOKEN=", tu)
        self.assertIn("[REDACTED:assign]", tu)
        self.assertNotIn("q7" * 28, tu)

    def test_redaction_keeps_ordinary_text(self):
        c = ING.Counter()
        for s in ["max_tokens: 1024", '"max_tokens": 128000000', "tokenizer=bert-base-uncased",
                  "TOKEN_FILE=/Users/x/.tushare_token", "sha256 8f86670e64eacbd7b15cb5fb0b5c1486317db0ea0d7cd496e557b7a35bbcfc80",
                  "commit f153acba", "https://www.anthropic.com/research/x", "risk-daily-builder"]:
            self.assertEqual(ING.redact(s, c), s, s)

    # ---- 可靠性 ----
    def test_bad_line_does_not_abort(self):
        self.assertEqual(self.ingest(), 0)
        self.assertIn("坏行 1", self.logs[-1])

    def test_source_read_only(self):
        before = snapshot(self.src)
        self.ingest()
        self.assertEqual(before, snapshot(self.src))

    def test_unreadable_file_does_not_abort_others(self):
        other = self.src / "-Users-x-proj" / "22222222-bbbb.jsonl"
        make_session(other, prefix="v")
        os.chmod(self.sess, 0)
        rc = self.ingest()
        self.assertEqual(rc, 1)
        self.assertIn("失败 1", self.logs[-1])
        self.assertEqual(len(read_out(self.dst)[0]), 1)
        os.chmod(self.sess, 0o644)
        self.assertEqual(self.ingest(), 0)
        self.assertEqual(len(read_out(self.dst)[0]), 2, "失败的文件下次应补上")

    def test_corrupt_state_rebuilds(self):
        self.ingest()
        (self.dst / "_state.json").write_text("{坏的", encoding="utf-8")
        self.assertEqual(self.ingest(), 0)
        self.assertTrue(any("状态文件损坏" in x for x in self.logs))
        self.assertTrue(list(self.dst.glob("_state.json.corrupt-*")))
        self.assertEqual(len(read_out(self.dst)[0]), 1, "重建后不应多出重复抽取件")

    def test_lock_blocks_second_run(self):
        self.dst.mkdir(parents=True)
        with open(self.dst / ".lock", "w") as f:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.assertEqual(self.ingest(), 3)
        self.assertEqual(self.ingest(), 0)

    # ---- 增量与保全 ----
    def test_incremental_skip_and_append(self):
        self.ingest()
        self.ingest()
        self.assertIn("新抽 0 · 更新 0 · 跳过 1", self.logs[-1])
        with open(self.sess, "a", encoding="utf-8") as f:
            f.write(line({"type": "user", "uuid": "u9", "timestamp": "2026-11-11T02:00:00Z",
                          "message": {"role": "user", "content": "追加的新内容 麒麟标记"}}))
        self.ingest()
        self.assertIn("更新 1", self.logs[-1])
        self.assertEqual(len(read_out(self.dst)[0]), 1)
        self.assertEqual(len(SEA.search(self.dst, "麒麟标记")), 1)

    def test_source_deleted_keeps_output(self):
        self.ingest()
        os.remove(self.sess)
        self.assertEqual(self.ingest(), 0)
        self.assertIn("抽取件保留 1", self.logs[-1])
        self.assertEqual(len(SEA.search(self.dst, "独角兽关键词")), 1)

    def test_shrunk_source_keeps_old_copy(self):
        self.ingest()
        self.sess.write_text(line({"type": "user", "uuid": "w1", "timestamp": "2026-11-12T00:00:00Z",
                                   "message": {"role": "user", "content": "改写后的短内容"}}), encoding="utf-8")
        self.ingest()
        self.assertIn("改写保全 1", self.logs[-1])
        self.assertEqual(len(read_out(self.dst)[0]), 2)
        self.assertEqual(len(SEA.search(self.dst, "独角兽关键词")), 1, "旧内容仍可检索")
        self.assertEqual(len(SEA.search(self.dst, "改写后的短内容")), 1)

    # ---- 来源 ----
    def test_cowork_source_filters(self):
        cw = self.root / "cowork"
        make_session(cw / "acct" / "ws" / "local_1" / ".claude" / "projects" / "-s" / "33333333-cccc.jsonl", prefix="c")
        make_session(cw / "acct" / "ws" / "local_1" / "audit.jsonl", prefix="c")
        make_session(cw / "acct" / "ws" / "local_1" / "outputs" / "fakebrain" / "mock.jsonl", prefix="m")
        sub = cw / "acct" / "ws" / "local_1" / ".claude" / "projects" / "-s" / "33333333-cccc" / "subagents" / "agent-1.jsonl"
        make_session(sub, prefix="s")
        sub.with_name("agent-1.meta.json").write_text(json.dumps({"agentType": "Explore", "description": "查找真相层"}), encoding="utf-8")
        self.ingest([("cowork", cw)])
        files, out = read_out(self.dst)
        self.assertEqual(len(files), 2, "只收 .claude/projects 下的会话与 subagent，不收 audit 与 outputs")
        heads = {o[0]["session_id"]: o[0] for o in out}
        self.assertEqual(heads["agent-1"]["agent_type"], "Explore")
        self.assertEqual(heads["agent-1"]["title"], "测试会话")
        self.assertEqual(heads["agent-1"]["agent_description"], "查找真相层")
        self.assertTrue(all(h["source"] == "cowork" for h in heads.values()))

    def test_multi_source_and_uid_dedupe(self):
        cp = self.root / "copy"
        make_session(cp / "local_9" / ".claude" / "projects" / "-p" / "44444444-dddd.jsonl")  # 与 code 来源同一批 uuid（模拟续接会话复制历史）
        self.ingest([("code", self.src), ("fuxi", cp)])
        self.assertEqual(len(read_out(self.dst)[0]), 2)
        self.assertEqual(len(SEA.search(self.dst, "独角兽关键词")), 1, "同 uid 只报一次")
        self.assertEqual(len(SEA.search(self.dst, "独角兽关键词", source="fuxi")), 1)

    def test_missing_src(self):
        self.assertEqual(ING.run([("x", self.root / "nope")], self.dst, log=self.logs.append), 2)

    # ---- 检索 ----
    def test_search_filters_and_miss(self):
        self.ingest()
        self.assertEqual(len(SEA.search(self.dst, "独角兽关键词")), 1)
        self.assertEqual(len(SEA.search(self.dst, "独角兽关键词", role="assistant")), 0)
        self.assertEqual(len(SEA.search(self.dst, "echo", kind="tool_use")), 1)
        self.assertEqual(len(SEA.search(self.dst, "不存在的词_qqq")), 0)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(SEA.main(["不存在的词_qqq", "--root", str(self.dst)]), 0)
        self.assertEqual(len(SEA.search(self.dst, r"独角兽.{2}词", regex=True)), 1)

    def test_search_uses_local_date(self):
        self.ingest()
        local = SEA.local_dt("2026-11-10T01:00:00Z")[:10]
        self.assertEqual(len(SEA.search(self.dst, "独角兽关键词", since=local, until=local)), 1)

    def test_corrupt_gz_skipped(self):
        self.ingest()
        bad = self.dst / "2026-11" / "2026-11-30_code_bad_0000000000.jsonl.gz"
        bad.write_bytes(gzip.compress(b'{"type":"header"}\n{"text":"x"}\n')[:20])
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(len(SEA.search(self.dst, "独角兽关键词")), 1)
        self.assertIn("已跳过", err.getvalue())

    def test_newest_first(self):
        self.ingest()
        later = self.src / "-Users-x-proj" / "99999999-zzzz.jsonl"
        later.write_text(line({"type": "user", "uuid": "z1", "timestamp": "2026-11-15T00:00:00Z",
                               "message": {"role": "user", "content": "共同词 新"}}), encoding="utf-8")
        with open(self.sess, "a", encoding="utf-8") as f:
            f.write(line({"type": "user", "uuid": "z0", "timestamp": "2026-11-10T03:00:00Z",
                          "message": {"role": "user", "content": "共同词 旧"}}))
        self.ingest()
        self.assertTrue(SEA.search(self.dst, "共同词")[0]["snippet"].endswith("新"))
        self.assertTrue(SEA.search(self.dst, "共同词", oldest_first=True)[0]["snippet"].endswith("旧"))


    # ---- v3：复审 N0–N7 ----
    def test_more_secret_forms(self):
        hx = "ab12" * 14  # 56 位假十六进制
        c = ING.Counter()
        cases = {
            "env_default": "TUSHARE_TOKEN = os.environ.get('TUSHARE_TOKEN', '" + hx + "')",
            "printf": "printf '%s' '" + hx + "' > ~/.tushare/token",
            "masked": "TUSHARE_TOKEN=******" + "cd34" * 11 + "ef",
            "masked2": "token: <前10位隐藏>" + "9a8b" * 11 + "7c",
            "pem_no_end": "-----BEGIN OPENSSH PRIVATE KEY-----\\nb3BlbnNzaC1rZXktdjEAAAAA" + "Q" * 60,
            "tos": "TOS_ACCESS_KEY=AKLT" + "Zm9v" * 6 + "12",
            "kimi": "KIMI_AUTH_TOKEN=****" + "x7Y8" * 10,
            "oss": "https://b.oss.example.com/f?OSSAccessKeyId=LTAI" + "5t6u" * 4 + "&Signature=ab%2Bcd" + "9" * 20 + "&Expires=1",
            "sts": "SecurityToken=CAIS" + "q1w2" * 8,
            "cookie_kv": "  odin_tt: " + "e5f6" * 40,
            "cookie_hdr": "Cookie: ttwid=1%7C" + "Rr" * 20 + "; sessionid=" + "5g" * 16,
        }
        leak = {"env_default": hx, "printf": hx, "masked": "cd34" * 11, "masked2": "9a8b" * 11,
                "pem_no_end": "Q" * 60, "tos": "Zm9v" * 6, "kimi": "x7Y8" * 10, "oss": "5t6u" * 4, "sts": "q1w2" * 8,
                "cookie_kv": "e5f6" * 40, "cookie_hdr": "Rr" * 20}
        for k, v in cases.items():
            out = ING.redact(v, c)
            self.assertNotIn(leak[k], out, f"{k} 泄漏：{out[:80]}")
            self.assertIn("[REDACTED:", out, k)

    def test_passwd_false_positives(self):
        c = ING.Counter()
        for s in ["PWD=/Users/x/proj", "\\nPWD=/Users/x", "password_reset_url=https://x.example/r",
                  "--password-file=/etc/pw", "password_hash=pbkdf2_sha256", "OLDPWD=/tmp"]:
            self.assertEqual(ING.redact(s, c), s, s)
        self.assertNotIn("x@Y!z9#w", ING.redact("DB_PASSWORD=x@Y!z9#w", c))

    def test_uid_fallback_no_collision(self):
        for n, word in (("55555555-eeee", "共同词A"), ("66666666-ffff", "共同词B")):
            (self.src / "-p" / f"{n}.jsonl").parent.mkdir(parents=True, exist_ok=True)
            (self.src / "-p" / f"{n}.jsonl").write_text(line({"type": "user", "timestamp": "2026-11-13T00:00:00Z",
                                                               "message": {"role": "user", "content": word}}), encoding="utf-8")
        self.ingest()
        self.assertEqual(len(SEA.search(self.dst, "共同词")), 2)

    def test_queued_time_window(self):
        extra = [line({"type": "user", "uuid": "e1", "timestamp": "2026-11-09T20:00:00Z",
                       "message": {"role": "user", "content": "继续"}}),
                 line({"type": "attachment", "uuid": "e2", "timestamp": "2026-11-10T02:00:00Z",
                       "attachment": {"type": "queued_command", "commandMode": "prompt", "prompt": "继续"}})]
        make_session(self.sess, extra=extra)
        self.ingest()
        self.assertEqual(sum(1 for r in self.recs() if r["text"] == "继续"), 2, "早先送达的同文消息不能吞掉后来的插话")

    def test_rewrite_larger_keeps_old(self):
        self.ingest()
        self.sess.write_text("".join(base_lines("r")) + line({"type": "user", "uuid": "r9", "timestamp": "2026-11-12T00:00:00Z",
                                                              "message": {"role": "user", "content": "更长的改写 青龙词 " + "填" * 500}}), encoding="utf-8")
        self.ingest()
        self.assertIn("改写保全 1", self.logs[-1])
        self.assertEqual(len(read_out(self.dst)[0]), 2)

    def test_corrupt_state_then_shrink_keeps_old(self):
        self.ingest()
        (self.dst / "_state.json").write_text("坏", encoding="utf-8")
        # 首条时间与原会话相同 → 输出路径相同，才能测到「覆盖同一抽取件」
        self.sess.write_text(line({"type": "user", "uuid": "k1", "timestamp": "2026-11-10T01:00:00Z",
                                   "message": {"role": "user", "content": "短"}}), encoding="utf-8")
        self.ingest()
        self.assertEqual(len(SEA.search(self.dst, "独角兽关键词")), 1, "状态损坏后源变小也不能丢旧内容")

    def test_dry_run_with_corrupt_state(self):
        self.ingest()
        (self.dst / "_state.json").write_text("坏", encoding="utf-8")
        self.assertEqual(ING.run([("code", self.src)], self.dst, dry_run=True, log=self.logs.append), 0)

    # ---- v4：第三轮复审 ----
    def test_v4_secret_forms(self):
        c = ING.Counter()
        ak = "AKLT" + "Nm9wcXJz" * 5 + "Q2"
        sk = "TkRVd" + "Ym1Fd09UZzNa" * 4 + "Rk1q"
        cases = [
            ("Access key ID：" + ak + ",secret key:" + sk, [ak[4:], sk]),
            ("SK：" + sk, [sk]),
            ('AK = "' + ak + '"\nSK = "' + sk + '"', [ak[4:], sk]),
            ("UIFID=" + "Qx7Lm2Pz" * 20 + "; bd_ticket_guard_client_data=" + "eyQ3" * 30, ["Qx7Lm2Pz" * 3, "eyQ3" * 5]),
            ("_bd_ticket_crypt_cookie=" + "0a1b" * 8, ["0a1b" * 8]),
            ("JSESSIONID=" + "9f8e" * 8 + "; gsessionid=" + "7d6c" * 6, ["9f8e" * 8, "7d6c" * 6]),
            ("../.env: line 21: " + "aZ3_" * 8 + ": command not found", ["aZ3_" * 8]),
            ("set-cookie: auth=" + "Tk9p" * 6 + "; Path=/", ["Tk9p" * 6]),
            ("裸串 " + "Xy9Kq2Lr8Wm4Np7Vb3Hc6Jd5Fg1Tz0Rs8Qa2Pw7Ue", ["Xy9Kq2Lr8Wm4Np7Vb3Hc6Jd5Fg1Tz0Rs8Qa2Pw7Ue"]),
            ("sig " + "Ab3+Cd4/Ef5Gh6+Ij7Kl8/Mn9Op0Qr1St2Uv3Wx4Yz5Aa6Bb7=", ["Ef5Gh6+Ij7Kl8"]),
            ("url /api/v1/" + "Zq8Wv2Xn5Bm7Lk3Jh9Gf4Dc1Sa6Pe0Ty4Ui7Op" + "/detail", ["Zq8Wv2Xn5Bm7Lk3Jh9Gf4Dc1Sa6Pe0Ty4Ui7Op"]),
        ]
        for text, leaks in cases:
            out = ING.redact(text, c)
            for v in leaks:
                self.assertNotIn(v, out, f"泄漏：{text[:40]} → {out[:80]}")

    def test_v4_false_positives(self):
        c = ING.Counter()
        keep = [
            '"sessionId":"8a1f0c2e-4b5d-4e6f-9a7b-1c2d3e4f5a6b"',
            "max_tokens: 1024 · sha256 " + "3c9d" * 16,
            "authored by bot, ref " + "a1b2c3d4" * 5,
            "object_key: reports/2026-11-19/daily.html",
            "cache_key=risk_daily_2026_11_19",
            "healthcheck_action_key: restart_2026_service",
            "var cookie=document.cookie.split(';')",
            "cookie: 已过期，需要重新登录",
            "os.environ.get('MONKEY_COUNT','bananas12345')",
            "tokenizer=bert-base-uncased-2026v1",
            "TOKEN_FILE=/Users/x/.config/tok_2026.txt",
            "sec_uid=MS4wLjABAAAA" + "Ab3dE" * 8,
            "enter_keyword: 2026Q3_report_final",
            "commit " + "f153acba" * 5 + " token budget ok",
            "token check passed, sha256: " + "5e6f" * 16,
            "toolu_01Y8G5FBb4A76N8aEFDT5hpL",
            'integrity="sha384-iRvT0SXzM4h7mQkxLlP9sP2t0wYbZ1q8VqkzXcLm3BnMh9mLQx3Z"',
            "encodeURIComponentForReport2026Version",
            "AI4ME/_misc/Report_Builder_2026_v2.html",
            "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/Index?type=web&code=SH600519",
            "/var/folders/zz/zyxvpxvq6csfxvn_n0000gn/T/claude-501/tool-results/webfetch-1795145486338-ccjiou.pdf",
            "/Users/lunarabbit/Library/Application Support/Claude-3p/local-agent-mode-sessions/27a35443-8af0-427c-9cae-f586ce3318fc/",
            "/Users/lunarabbit/Documents/Claude/brain/.tools/transcript_ingest.py",
        ]
        for s in keep:
            self.assertEqual(ING.redact(s, c), s, s)

    def test_queued_then_delivered_no_superseded(self):
        q = line({"type": "attachment", "uuid": "qq1", "timestamp": "2026-11-10T05:00:00Z",
                  "attachment": {"type": "queued_command", "commandMode": "prompt", "prompt": "插话玄机"}})
        make_session(self.sess, extra=[q])
        self.ingest()
        with open(self.sess, "a", encoding="utf-8") as f:
            f.write(line({"type": "user", "uuid": "qq2", "timestamp": "2026-11-10T05:00:30Z",
                          "message": {"role": "user", "content": "插话玄机"}}))
        self.ingest()
        self.assertNotIn("改写保全 1", self.logs[-1])
        self.assertEqual(len(SEA.search(self.dst, "插话玄机")), 1)

    def test_source_glob(self):
        cp = self.root / "arch"
        make_session(cp / "local_1" / ".claude" / "projects" / "-p" / "77777777-gggg.jsonl", prefix="g")
        self.ingest([("code", self.src), ("fuxi-20260811", cp)])
        self.assertEqual(len(SEA.search(self.dst, "独角兽关键词", source="fuxi-*")), 1)
        self.assertEqual(len(SEA.search(self.dst, "独角兽关键词", source="cowork*")), 0)

    # ---- v5：已知凭证黑名单与第四轮复审 ----
    def test_known_secret_fragments(self):
        tok = "3fa9c1" + "e7b24d80" * 6 + "5c"  # 56 位假令牌
        envf = self.root / "secrets" / ".env"
        envf.parent.mkdir()
        envf.write_text("export TUSHARE_TOKEN='" + tok + "'\nTOS_ENDPOINT=tos-cn-beijing.volces.com\n", encoding="utf-8")
        srcf = self.root / "sources.txt"
        srcf.write_text(str(envf) + "\n", encoding="utf-8")
        vals, nf = ING.load_known_secrets(srcf)
        self.assertEqual((nf, vals), (1, [tok]), "只取凭证值，不取 endpoint")
        ING.set_known_secrets(vals)
        try:
            c = ING.Counter()
            for text in ["TUSHARE_TOKEN=****(redacted)" + tok[8:],      # 后 48 位
                         "token 前缀 " + tok[:8] + " 已核",              # 前 8 位
                         "grep -r '" + tok[:16] + "' .",                 # 前 16 位
                         "全值 " + tok]:
                out = ING.redact(text, c)
                for k in range(0, len(tok) - 8 + 1):
                    self.assertNotIn(tok[k:k + 8], out, f"碎片泄漏：{out[:60]}")
            self.assertEqual(ING.redact("tos-cn-beijing.volces.com", c), "tos-cn-beijing.volces.com")
        finally:
            ING.set_known_secrets([])

    def test_known_secrets_via_run(self):
        envf = self.root / "k.token"
        envf.write_text("Kq7" + "x9Lm2Pz4" * 5 + "\n", encoding="utf-8")
        srcf = self.root / "sources.txt"
        srcf.write_text(str(envf) + "\n", encoding="utf-8")
        make_session(self.sess, extra=[line({"type": "user", "uuid": "kk", "timestamp": "2026-11-10T06:00:00Z",
                                             "message": {"role": "user", "content": "看这个 " + "x9Lm2Pz4" * 3}})])
        ING.run([("code", self.src)], self.dst, log=self.logs.append, secret_sources=srcf)
        ING.set_known_secrets([])
        self.assertTrue(any("已知凭证黑名单：1 个值" in x for x in self.logs))
        blob = json.dumps(read_out(self.dst)[1], ensure_ascii=False)
        self.assertNotIn("x9Lm2Pz4", blob)
        self.assertIn("[REDACTED:known]", blob)
        self.assertFalse(any("x9Lm2Pz4" in x for x in self.logs), "日志里不得出现凭证值")

    def test_partial_mask_and_hex_adjacency(self):
        c = ING.Counter()
        cases = {
            "TUSHARE_TOKEN=****(redacted)" + "ab12cd34" * 6: "ab12cd34" * 6,
            "TUSHARE_TOKEN=<前10位隐藏>" + "9f8e7d6c" * 5 + "5b4a3c2d1e0f": "9f8e7d6c" * 5,
            "tushare的token是" + "0a1b2c3d" * 5: "0a1b2c3d" * 5,
            "令牌：" + "e5f6a7b8" * 4: "e5f6a7b8" * 4,
            "MY_TUSHARE_TOKEN " + "c0ffee12" * 6: "c0ffee12" * 6,
        }
        for text, leak in cases.items():
            self.assertNotIn(leak, ING.redact(text, c), text[:30])

    def test_new_prefixes(self):
        c = ING.Counter()
        for v in ["LTAI5t" + "Gh7Kp2Qz9Wx4", "glpat-" + "Ab3Cd4Ef5Gh6Ij7Kl8Mn", "hf_" + "Zz9Yy8Xx7Ww6Vv5Uu4Tt3Ss2Rr1Qq0Pp",
                  "ntn_" + "123456789012" + "AbCdEfGhIjKlMnOpQrSt", "0123456789abcdef0123456789abcdef.AbCdEfGh12345678"]:
            self.assertNotIn(v, ING.redact("key " + v + " end", c), v[:8])

    def test_title_redacted(self):
        t = "sk-ant-api03-" + "T" * 30
        self.sess.write_text(line({"type": "ai-title", "aiTitle": "配置 " + t}) + "".join(base_lines()), encoding="utf-8")
        self.ingest()
        self.assertNotIn("T" * 30, json.dumps(read_out(self.dst)[1][0][0], ensure_ascii=False))

    def test_dry_run_non_dict_state(self):
        self.ingest()
        (self.dst / "_state.json").write_text("[1, 2]", encoding="utf-8")
        self.assertEqual(ING.run([("code", self.src)], self.dst, dry_run=True, log=self.logs.append), 0)

    def test_narrowed_highent_keeps_ids(self):
        c = ING.Counter()
        for s in ["SESSION_ID=8a1f0c2e-4b5d-4e6f-9a7b-1c2d3e4f5a6b", "https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf",
                  "?utm_source=wx&csrf=Ab3dE5fG7hJ9kL1mN3pQ", "backtest_2026Q3_rsi14_ma60_v2", "-Users-lunarabbit-Documents-Claude-brain"]:
            self.assertEqual(ING.redact(s, c), s, s)

    # ---- v6：第五轮复审 ----
    def _write_sources(self, files):
        srcf = self.root / "srcs.txt"
        srcf.write_text("\n".join(str(f) for f in files) + "\n", encoding="utf-8")
        return srcf

    def test_fail_closed_missing_list(self):
        rc = ING.run([("code", self.src)], self.dst, log=self.logs.append, secret_sources=self.root / "nope.txt")
        self.assertEqual(rc, 4)
        self.assertFalse(list(self.dst.rglob("*.jsonl.gz")), "黑名单没加载起来时不得写抽取件")
        self.assertTrue(any("黑名单加载异常" in x for x in self.logs))

    def test_fail_closed_unreadable_and_shrink(self):
        a = self.root / "a.env"; a.write_text("TUSHARE_TOKEN=Ab12Cd34Ef56Gh78Ij90\n", encoding="utf-8")
        b = self.root / "b.env"; b.write_text("API_KEY=Zz99Yy88Xx77Ww66Vv55\n", encoding="utf-8")
        srcf = self._write_sources([a, b])
        self.assertEqual(ING.run([("code", self.src)], self.dst, log=self.logs.append, secret_sources=srcf), 0)
        os.chmod(b, 0)
        try:
            self.assertEqual(ING.run([("code", self.src)], self.dst, log=self.logs.append, secret_sources=srcf), 4)
            self.assertIn("读取失败", self.logs[-1])
        finally:
            os.chmod(b, 0o644)
        b.unlink()
        self.assertEqual(ING.run([("code", self.src)], self.dst, log=self.logs.append, secret_sources=srcf), 4)
        self.assertIn("比上次少", self.logs[-1])
        self.assertEqual(ING.run([("code", self.src)], self.dst, log=self.logs.append, secret_sources=srcf,
                                 accept_secret_change=True), 0)
        ING.set_known_secrets([])

    def test_loader_value_filters(self):
        e = self.root / "x.env"
        e.write_text("\n".join([
            "APIYI_AUTH_HEADER=Authorization",
            "COOKIE_DOMAIN=api.example-host.com",
            "DASHSCOPE_KEY=<your-dashscope-key>",
            "DATABASE_URL=postgres://dev:dev@localhost:5432/app",
            "OPENAI_IMAGE2_API_KEY_ENV=OPENAI_API_KEY",
            "LLM_API_KEY=<sk-9f8e7d6c5b4a39281706f5e4d3c2b1a0>",
            "AWS_KEY=AKIA1234567890ABCDEF",
        ]) + "\n", encoding="utf-8")
        t = self.root / "t.token"; t.write_text("QWxhZGRpbjpvcGVuIHNlc2FtZQ==\n", encoding="utf-8")
        vals, nf = ING.load_known_secrets(self._write_sources([e, t]))
        self.assertEqual(nf, 2)
        self.assertEqual(sorted(vals), sorted(["sk-9f8e7d6c5b4a39281706f5e4d3c2b1a0", "AKIA1234567890ABCDEF", "QWxhZGRpbjpvcGVuIHNlc2FtZQ=="]))

    def test_known_windows_across_special_chars(self):
        v = "Pa55w0rd!Xy9Kq2Lr8Wm"
        ING.set_known_secrets([v])
        try:
            out = ING.redact("口令片段 Xy9Kq2Lr8Wm 和 Pa55w0rd", ING.Counter())
            self.assertNotIn("Xy9Kq2Lr8Wm", out)
        finally:
            ING.set_known_secrets([])

    def test_v6_rule_fixes(self):
        c = ING.Counter()
        self.assertEqual(ING.redact("https://x.com/samsung-sk-hynix-hbm4-shipments-2026-report", c),
                         "https://x.com/samsung-sk-hynix-hbm4-shipments-2026-report")
        for text, leak in [("数据库密码：Qw3rty!Zx9Cv8", "Qw3rty!Zx9Cv8"), ("令牌：Ab3dEf5gHi7jKl9m", "Ab3dEf5gHi7jKl9m"),
                           ("密钥是 Zz9yY8xX7wW6vV5uU4", "Zz9yY8xX7wW6vV5uU4"), ("token＝Ab12Cd34Ef56Gh78Ij", "Ab12Cd34Ef56Gh78Ij"),
                           ("api_key: …Ab12Cd34Ef56Gh78Ij90", "Ab12Cd34Ef56Gh78Ij90")]:
            self.assertNotIn(leak, ING.redact(text, c), text)
        self.assertEqual(ING.redact("密钥是否需要轮换，还没定", c), "密钥是否需要轮换，还没定")

    # ---- v7：检索给 Dream 用的三项 ----
    def test_search_exclude_notes_and_batch(self):
        extra = [
            line({"type": "assistant", "uuid": "n1", "timestamp": "2026-11-10T07:00:00Z", "message": {"role": "assistant", "content": [
                {"type": "tool_use", "id": "w1", "name": "Write",
                 "input": {"file_path": "/Users/x/Documents/Claude/brain/logs/2026-11-10-a.md", "content": "照草案写的结论 青鸾词"}}]}}),
            line({"type": "user", "uuid": "n2", "timestamp": "2026-11-10T07:00:01Z", "message": {"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": "w1", "content": "写入成功 青鸾词"}]}}),
            line({"type": "user", "uuid": "n3", "timestamp": "2026-11-10T07:01:00Z",
                  "message": {"role": "user", "content": "Doctor 原话 青鸾词"}}),
        ]
        make_session(self.sess, extra=extra)
        self.ingest()
        self.assertEqual(len(SEA.search(self.dst, "青鸾词")), 3)
        hits = SEA.search(self.dst, "青鸾词", exclude_notes=True)
        self.assertEqual([h["role"] for h in hits], ["user"], "笔记自身的写入与结果被排除，只剩 Doctor 原话")
        self.assertEqual(hits[0]["kind"], "text")
        multi = SEA.search(self.dst, None, patterns=["独角兽关键词", "青鸾词"], limit=0)
        self.assertEqual(sorted({h["pattern"] for h in multi}), ["独角兽关键词", "青鸾词"])

    def test_search_header_time_skip(self):
        self.ingest()
        local = SEA.local_dt("2026-11-10T01:00:00Z")[:10]
        self.assertEqual(len(SEA.search(self.dst, "独角兽关键词", since="2026-12-01")), 0)
        self.assertEqual(len(SEA.search(self.dst, "独角兽关键词", until="2026-11-01")), 0)
        self.assertEqual(len(SEA.search(self.dst, "独角兽关键词", since=local)), 1)

    def test_v7_rule_fixes(self):
        c = ING.Counter()
        for s in ["SK=/sessions/abc123/mnt/Documents/Claude", 'SK="/Users/x/Library/Application Support/2026"',
                  "https://www.reuters.com/sk-hynix-hbm4-shipments-2026-report", "ssh: password:\nLast login: Thu Nov 19 2026 from 192.168.1.10"]:
            self.assertEqual(ING.redact(s, c), s, s)
        for text, leak in [("token: `Ab12Cd34Ef56Gh78Ij`", "Ab12Cd34Ef56Gh78Ij"), ("**Token**: Ab12Cd34Ef56Gh78Ij90", "Ab12Cd34Ef56Gh78Ij90"),
                           ("--token Zz99Yy88Xx77Ww66", "Zz99Yy88Xx77Ww66"), ("api_key=“Ab12Cd34Ef56Gh78Ij90”", "Ab12Cd34Ef56Gh78Ij90"),
                           ("令牌（Tushare）：e5f6a7b8c9d0e1f2", "e5f6a7b8c9d0e1f2"), ("sk-or-v1-" + "ab12" * 16, "ab12" * 16)]:
            self.assertNotIn(leak, ING.redact(text, c), text)

    def test_unreadable_secret_list_and_sidecar_baseline(self):
        a = self.root / "a.env"; a.write_text("TUSHARE_TOKEN=Ab12Cd34Ef56Gh78Ij90\nAPI_KEY=Zz99Yy88Xx77Ww66Vv55\n", encoding="utf-8")
        srcf = self.root / "srcs.txt"; srcf.write_text(str(a) + "\n", encoding="utf-8")
        self.assertEqual(ING.run([("code", self.src)], self.dst, log=self.logs.append, secret_sources=srcf), 0)
        os.chmod(srcf, 0)
        try:
            self.assertEqual(ING.run([("code", self.src)], self.dst, log=self.logs.append, secret_sources=srcf), 4)
        finally:
            os.chmod(srcf, 0o644)
        (self.dst / "_state.json").write_text("坏", encoding="utf-8")
        a.write_text("TUSHARE_TOKEN=Ab12Cd34Ef56Gh78Ij90\n", encoding="utf-8")
        self.assertEqual(ING.run([("code", self.src)], self.dst, log=self.logs.append, secret_sources=srcf), 4,
                         "状态文件损坏后基线从旁路文件取回，值变少仍被拦下")
        ING.set_known_secrets([])

    def test_search_exclude_single_path_keeps_other_evidence(self):
        extra = [
            line({"type": "assistant", "uuid": "p1", "timestamp": "2026-11-10T08:00:00Z", "message": {"role": "assistant", "content": [
                {"type": "tool_use", "id": "e1", "name": "Edit",
                 "input": {"file_path": "/Users/x/Documents/Claude/brain/permanent/CC声音档案.md", "old_string": "a", "new_string": "落改两处 白鹭词"}},
                {"type": "tool_use", "id": "w2", "name": "Write",
                 "input": {"file_path": "/Users/x/Documents/Claude/brain/logs/2026-11-10-b.md", "content": "落改两处 白鹭词"}}]}}),
            line({"type": "user", "uuid": "p2", "timestamp": "2026-11-10T08:00:02Z", "message": {"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": "g1", "content": "logs/2026-11-10-b.md:3: 落改两处 白鹭词"}]}}),
        ]
        make_session(self.sess, extra=extra)
        self.ingest()
        hits = SEA.search(self.dst, "白鹭词", exclude_paths=["logs/2026-11-10-b.md"])
        self.assertEqual([h["tool"] for h in hits], ["Edit"], "只排除核对中这篇日志自己的写入与带它路径的输出，别的文件的 Edit 是证据要留")

if __name__ == "__main__":
    unittest.main(verbosity=2)
