
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api, authStorage } from "../api";

export default function Signup() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    if (password.length < 8) {
      setError("Password must contain at least 8 characters.");
      return;
    }

    setLoading(true);

    try {
      const data = await api.signup({ name, email, password });
      authStorage.save(data);
      navigate("/", { replace: true });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-[#0f1419] text-[#e6e8eb] flex items-center justify-center px-5 py-8">
      <div className="w-full max-w-md rounded-xl border border-[#2a313c] bg-[#151b23] p-8 shadow-xl">
        <div className="mb-8">
          <div className="flex gap-1.5 mb-4">
            <span className="h-2 w-2 rounded-full bg-blue-400" />
            <span className="h-2 w-2 rounded-full bg-cyan-400" />
            <span className="h-2 w-2 rounded-full bg-violet-400" />
          </div>
          <h1 className="text-2xl font-semibold">Create your account</h1>
          <p className="mt-2 text-sm text-gray-400">
            Start managing your LLM costs intelligently.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="mb-2 block text-sm">Full name</label>
            <input
              required
              minLength={2}
              maxLength={100}
              autoComplete="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full rounded-md border border-[#303a48] bg-[#0f1419] px-3 py-3 text-sm outline-none focus:border-blue-500"
              placeholder="Your name"
            />
          </div>

          <div>
            <label className="mb-2 block text-sm">Email address</label>
            <input
              type="email"
              required
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded-md border border-[#303a48] bg-[#0f1419] px-3 py-3 text-sm outline-none focus:border-blue-500"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label className="mb-2 block text-sm">Password</label>
            <input
              type="password"
              required
              minLength={8}
              maxLength={128}
              autoComplete="new-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-md border border-[#303a48] bg-[#0f1419] px-3 py-3 text-sm outline-none focus:border-blue-500"
              placeholder="At least 8 characters"
            />
          </div>

          {error && (
            <p role="alert" className="rounded-md border border-red-900 bg-red-950/40 p-3 text-sm text-red-300">
              {error}
            </p>
          )}

          <button
            disabled={loading}
            className="w-full rounded-md bg-blue-600 py-3 text-sm font-medium hover:bg-blue-500 disabled:opacity-50"
          >
            {loading ? "Creating account..." : "Create account"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-gray-400">
          Already registered?{" "}
          <Link to="/login" className="text-blue-400 hover:text-blue-300">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}