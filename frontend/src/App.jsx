import { useState } from "react"
import axios from "axios"
import { useDropzone } from "react-dropzone"
import { RadialBarChart, RadialBar, ResponsiveContainer } from "recharts"
import { FileText, Briefcase, Brain, ChevronRight, AlertCircle, CheckCircle, BookOpen } from "lucide-react"

const API = "https://resume-screener-0er2.onrender.com"

function ScoreGauge({ score }) {
  const data = [{ value: score, fill: score >= 75 ? "#22c55e" : score >= 50 ? "#f59e0b" : score >= 30 ? "#f97316" : "#ef4444" }]
  return (
    <div className="flex flex-col items-center">
      <ResponsiveContainer width={200} height={200}>
        <RadialBarChart cx="50%" cy="50%" innerRadius="60%" outerRadius="100%" data={data} startAngle={90} endAngle={-270}>
          <RadialBar dataKey="value" max={100} />
        </RadialBarChart>
      </ResponsiveContainer>
      <div className="text-5xl font-bold -mt-24">{score}%</div>
      <div className="mt-16 text-lg font-semibold text-slate-300">Match Score</div>
    </div>
  )
}

function SkillBadge({ skill, type }) {
  const colors = {
    match: "bg-green-500/20 text-green-400 border border-green-500/30",
    missing: "bg-red-500/20 text-red-400 border border-red-500/30",
    neutral: "bg-blue-500/20 text-blue-400 border border-blue-500/30"
  }
  return (
    <span className={`px-3 py-1 rounded-full text-sm font-medium ${colors[type]}`}>
      {skill}
    </span>
  )
}

export default function App() {
  const [file, setFile] = useState(null)
  const [jobDesc, setJobDesc] = useState("")
  const [jobTitle, setJobTitle] = useState("")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: { "application/pdf": [".pdf"] },
    maxFiles: 1,
    onDrop: (files) => setFile(files[0])
  })

  const handleAnalyze = async () => {
    if (!file || !jobDesc) {
      setError("Please upload a resume and enter a job description!")
      return
    }
    setError("")
    setLoading(true)
    setResult(null)

    const formData = new FormData()
    formData.append("resume", file)
    formData.append("job_description", jobDesc)
    formData.append("job_title", jobTitle)

    try {
      const res = await axios.post(`${API}/analyze`, formData)
      setResult(res.data)
    } catch (err) {
      setError("Something went wrong! Make sure backend is running.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen p-6 max-w-5xl mx-auto">
      {/* Header */}
      <div className="text-center mb-10">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
          AI Resume Screener
        </h1>
        <p className="text-slate-400 mt-2">Upload your resume and match it against any job description</p>
      </div>

      {/* Input Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        {/* Resume Upload */}
        <div className="bg-slate-800 rounded-2xl p-6">
          <div className="flex items-center gap-2 mb-4">
            <FileText className="text-blue-400" size={20} />
            <h2 className="font-semibold text-lg">Upload Resume</h2>
          </div>
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all
              ${isDragActive ? "border-blue-400 bg-blue-500/10" : "border-slate-600 hover:border-blue-400"}`}
          >
            <input {...getInputProps()} />
            {file ? (
              <div className="text-green-400">
                <CheckCircle className="mx-auto mb-2" size={32} />
                <p className="font-medium">{file.name}</p>
                <p className="text-sm text-slate-400 mt-1">Click to change</p>
              </div>
            ) : (
              <div className="text-slate-400">
                <FileText className="mx-auto mb-2" size={32} />
                <p>Drag & drop your PDF resume here</p>
                <p className="text-sm mt-1">or click to browse</p>
              </div>
            )}
          </div>
        </div>

        {/* Job Description */}
        <div className="bg-slate-800 rounded-2xl p-6">
          <div className="flex items-center gap-2 mb-4">
            <Briefcase className="text-purple-400" size={20} />
            <h2 className="font-semibold text-lg">Job Description</h2>
          </div>
          <input
            type="text"
            placeholder="Job Title (e.g. ML Engineer)"
            value={jobTitle}
            onChange={(e) => setJobTitle(e.target.value)}
            className="w-full bg-slate-700 rounded-xl px-4 py-2 mb-3 text-sm outline-none focus:ring-2 ring-purple-500"
          />
          <textarea
            placeholder="Paste the full job description here..."
            value={jobDesc}
            onChange={(e) => setJobDesc(e.target.value)}
            rows={6}
            className="w-full bg-slate-700 rounded-xl px-4 py-2 text-sm outline-none focus:ring-2 ring-purple-500 resize-none"
          />
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="flex items-center gap-2 text-red-400 bg-red-500/10 border border-red-500/30 rounded-xl px-4 py-3 mb-4">
          <AlertCircle size={18} />
          {error}
        </div>
      )}

      {/* Analyze Button */}
      <button
        onClick={handleAnalyze}
        disabled={loading}
        className="w-full py-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl font-semibold text-lg
          hover:opacity-90 transition-all disabled:opacity-50 flex items-center justify-center gap-2"
      >
        {loading ? (
          <>
            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            Analyzing with AI...
          </>
        ) : (
          <>
            <Brain size={20} />
            Analyze Resume
            <ChevronRight size={20} />
          </>
        )}
      </button>

      {/* Results */}
      {result && result.success && (
        <div className="mt-10 space-y-6">
          {/* Score */}
          <div className="bg-slate-800 rounded-2xl p-8 flex flex-col items-center">
            <ScoreGauge score={result.match_result.final_score} />
            <div className="mt-4 text-2xl font-bold">{result.match_result.verdict}</div>
            <div className="grid grid-cols-2 gap-4 mt-6 w-full max-w-sm">
              <div className="bg-slate-700 rounded-xl p-4 text-center">
                <div className="text-2xl font-bold text-blue-400">{result.match_result.tfidf_score}%</div>
                <div className="text-sm text-slate-400 mt-1">TF-IDF Score</div>
              </div>
              <div className="bg-slate-700 rounded-xl p-4 text-center">
                <div className="text-2xl font-bold text-purple-400">{result.match_result.semantic_score}%</div>
                <div className="text-sm text-slate-400 mt-1">Semantic Score</div>
              </div>
            </div>
          </div>

          {/* Skills */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-slate-800 rounded-2xl p-6">
              <h3 className="font-semibold text-green-400 mb-4 flex items-center gap-2">
                <CheckCircle size={18} /> Matching Skills ({result.match_result.matching_skills.length})
              </h3>
              <div className="flex flex-wrap gap-2">
                {result.match_result.matching_skills.length > 0
                  ? result.match_result.matching_skills.map(s => <SkillBadge key={s} skill={s} type="match" />)
                  : <p className="text-slate-400 text-sm">No matching skills found</p>}
              </div>
            </div>
            <div className="bg-slate-800 rounded-2xl p-6">
              <h3 className="font-semibold text-red-400 mb-4 flex items-center gap-2">
                <AlertCircle size={18} /> Missing Skills ({result.match_result.missing_skills.length})
              </h3>
              <div className="flex flex-wrap gap-2">
                {result.match_result.missing_skills.length > 0
                  ? result.match_result.missing_skills.map(s => <SkillBadge key={s} skill={s} type="missing" />)
                  : <p className="text-slate-400 text-sm">No missing skills!</p>}
              </div>
            </div>
          </div>

          {/* Resume Info */}
          <div className="bg-slate-800 rounded-2xl p-6">
            <h3 className="font-semibold text-blue-400 mb-4 flex items-center gap-2">
              <FileText size={18} /> Resume Info
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-slate-700 rounded-xl p-3 text-center">
                <div className="text-xl font-bold">{result.resume_info.word_count}</div>
                <div className="text-xs text-slate-400 mt-1">Words</div>
              </div>
              <div className="bg-slate-700 rounded-xl p-3 text-center">
                <div className="text-xl font-bold">{result.resume_info.skills.length}</div>
                <div className="text-xs text-slate-400 mt-1">Skills Found</div>
              </div>
              <div className="bg-slate-700 rounded-xl p-3 text-center">
                <div className="text-sm font-medium truncate">{result.resume_info.email || "N/A"}</div>
                <div className="text-xs text-slate-400 mt-1">Email</div>
              </div>
              <div className="bg-slate-700 rounded-xl p-3 text-center">
                <div className="text-sm font-medium">{result.resume_info.education.join(", ") || "N/A"}</div>
                <div className="text-xs text-slate-400 mt-1">Education</div>
              </div>
            </div>
          </div>

          {/* AI Advice */}
          {result.ai_advice.success && (
            <div className="bg-slate-800 rounded-2xl p-6">
              <h3 className="font-semibold text-purple-400 mb-6 flex items-center gap-2">
                <Brain size={18} /> AI Career Advice
              </h3>
              <div className="space-y-4">
                {[
                  { key: "assessment", label: "📊 Assessment", color: "blue" },
                  { key: "skills_to_learn", label: "📚 Skills To Learn", color: "green" },
                  { key: "resume_tips", label: "📝 Resume Tips", color: "yellow" },
                  { key: "interview_tips", label: "🎯 Interview Tips", color: "purple" }
                ].map(({ key, label, color }) => (
                  result.ai_advice.advice[key] && (
                    <div key={key} className="bg-slate-700 rounded-xl p-4">
                      <h4 className="font-semibold mb-2">{label}</h4>
                      <p className="text-slate-300 text-sm whitespace-pre-line">
                        {result.ai_advice.advice[key]}
                      </p>
                    </div>
                  )
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}