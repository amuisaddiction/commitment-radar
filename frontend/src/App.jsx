import { useEffect, useMemo, useState } from "react";
import {
  Activity, AlertTriangle, ArrowDownRight, ArrowUpRight, Bell,
  CalendarDays, Check, CheckCircle2, ChevronDown, CircleHelp,
  Clock3, Command, Database, FileText, Filter, LayoutDashboard,
  Link2, ListChecks, MessageSquareText, Mic, MoreHorizontal,
  Plus, Search, Settings2, ShieldCheck, Sparkles, Trash2, Workflow,
  X
} from "lucide-react";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const initialCommitments = [
  {
    id: "demo-1", task: "Send Rahul the invoice", owner: "You",
    deadline: "2026-10-12T17:00:00", status: "At risk",
    source_text: "I'll send Rahul the invoice by Friday.",
    created: "Mon, 9:42 AM", tag: "Finance", demo: true
  },
  {
    id: "demo-2", task: "Book the project venue", owner: "You",
    deadline: "2026-10-15T12:00:00", status: "On track",
    source_text: "I'll confirm the venue booking by Thursday.",
    created: "Today, 10:18 AM", tag: "Project", demo: true
  },
  {
    id: "demo-3", task: "Share the revised proposal", owner: "You",
    deadline: "2026-10-14T15:00:00", status: "On track",
    source_text: "I'll send over the revised proposal on Wednesday afternoon.",
    created: "Yesterday, 4:06 PM", tag: "Client", demo: true
  }
];

const initialActivity = [
  { icon: "memory", title: "Related commitment retrieved", detail: "Invoice deadline · Qdrant adapter pending", time: "Just now" },
  { icon: "agent", title: "Workflow scaffold ready", detail: "Real Lyzr orchestration is not yet connected", time: "Just now" },
  { icon: "voice", title: "Transcript source", detail: "Sample data · not a live Omi capture", time: "Today" }
];

function Icon({ name, size = 18 }) {
  const icons = {
    dashboard: LayoutDashboard, list: ListChecks, voice: Mic, activity: Activity,
    settings: Settings2, bell: Bell, search: Search, filter: Filter, plus: Plus,
    calendar: CalendarDays, clock: Clock3, alert: AlertTriangle, check: Check,
    arrowUp: ArrowUpRight, arrowDown: ArrowDownRight, message: MessageSquareText,
    database: Database, agent: Workflow, memory: Database, link: Link2,
    file: FileText, shield: ShieldCheck, sparkle: Sparkles, help: CircleHelp,
    more: MoreHorizontal, trash: Trash2, close: X, command: Command,
    chevron: ChevronDown, checkCircle: CheckCircle2
  };
  const Component = icons[name] || Activity;
  return <Component size={size} strokeWidth={1.8} aria-hidden="true" />;
}

function Badge({ children, tone = "neutral" }) {
  return <span className={`badge badge-${tone}`}><span className="badge-dot" />{children}</span>;
}

function Sidebar({ active, setActive }) {
  const nav = [
    { id: "overview", label: "Overview", icon: "dashboard" },
    { id: "commitments", label: "Commitments", icon: "list", count: "12" },
    { id: "voice", label: "Voice inbox", icon: "voice", count: "3" },
    { id: "activity", label: "Agent activity", icon: "activity" }
  ];
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-mark"><Icon name="command" size={21} /></div>
        <div><strong>commitment<span>radar</span></strong><small>PERSONAL WORKSPACE</small></div>
      </div>
      <div className="workspace-switch">
        <div className="avatar avatar-indigo">AY</div>
        <div className="workspace-copy"><strong>Amrita's workspace</strong><span>Personal plan</span></div>
        <Icon name="chevron" size={15} />
      </div>
      <div className="nav-label">WORKSPACE</div>
      <nav className="nav-list">
        {nav.map(item => (
          <button key={item.id} className={`nav-item ${active === item.id ? "active" : ""}`} onClick={() => setActive(item.id)}>
            <Icon name={item.icon} size={18} /><span>{item.label}</span>
            {item.count && <span className="nav-count">{item.count}</span>}
          </button>
        ))}
      </nav>
      <div className="nav-label nav-label-spaced">PREFERENCES</div>
      <button className={`nav-item ${active === "settings" ? "active" : ""}`} onClick={() => setActive("settings")}><Icon name="settings" /><span>Settings & integrations</span></button>
      <div className="sidebar-bottom">
        <div className="privacy-card">
          <div className="privacy-icon"><Icon name="shield" size={17} /></div>
          <strong>Your words, your control</strong>
          <p>Review what gets remembered. Remove anything you no longer need.</p>
          <button onClick={() => setActive("settings")}>Privacy settings <span>→</span></button>
        </div>
        <div className="profile">
          <div className="avatar avatar-rose">AY</div>
          <div className="profile-copy"><strong>Amrita Yadav</strong><span>Personal workspace</span></div>
          <Icon name="more" size={18} />
        </div>
      </div>
    </aside>
  );
}

function StatCard({ label, value, note, icon, tone, trend }) {
  return (
    <div className="stat-card">
      <div className="stat-top"><span>{label}</span><div className={`stat-icon ${tone}`}><Icon name={icon} size={18} /></div></div>
      <div className="stat-value">{value}</div>
      <div className="stat-note"><span className={`trend ${trend === "down" ? "trend-down" : ""}`}><Icon name={trend === "down" ? "arrowDown" : "arrowUp"} size={13} /> {note.split(" ")[0]}</span> {note.split(" ").slice(1).join(" ")}</div>
    </div>
  );
}

function StatusBadge({ status }) {
  const tone = status === "At risk" ? "warning" : status === "Completed" ? "success" : "info";
  return <Badge tone={tone}>{status}</Badge>;
}

function Overview({ commitments, activity, onOpenCommitment, onShowIngest, apiStatus }) {
  const riskCount = commitments.filter(c => c.status === "At risk").length;
  return (
    <>
      <div className="page-heading">
        <div><div className="eyebrow"><span className="eyebrow-line" /> MONDAY, OCTOBER 12, 2026</div><h1>Good morning, Amrita <span className="wave">✳</span></h1><p>Keep your promises in view. We'll help you spot the ones that need attention.</p></div>
        <button className="btn btn-primary" onClick={onShowIngest}><Icon name="plus" size={17} /> Add a commitment</button>
      </div>
      <div className="demo-banner"><span className="demo-pill">DEMO MODE</span><span>Sample dashboard data is shown. Live Omi, Qdrant and Lyzr integrations must be configured and verified.</span><button onClick={() => window.open(`${API_BASE}/health`, "_blank", "noopener,noreferrer")}>Check API status <Icon name="arrowUp" size={13} /></button></div>
      <section className="stats-grid">
        <StatCard label="Open commitments" value={String(commitments.length).padStart(2, "0")} note="8% from last week" icon="list" tone="violet" />
        <StatCard label="Need attention" value={String(riskCount).padStart(2, "0")} note="Review these today" icon="alert" tone="amber" trend="down" />
        <StatCard label="Completed this week" value="08" note="2 more than last week" icon="checkCircle" tone="green" />
        <StatCard label="Voice notes captured" value="14" note="3 awaiting review" icon="voice" tone="blue" />
      </section>
      <section className="content-grid">
        <div className="panel commitment-panel">
          <div className="panel-header"><div><h2>Commitments to keep</h2><p>Your promises, organized by what needs attention.</p></div><button className="text-button" onClick={() => onOpenCommitment("all")}>View all <span>→</span></button></div>
          <div className="table-wrap">
            <table>
              <thead><tr><th>COMMITMENT</th><th>DUE DATE</th><th>STATUS</th><th></th></tr></thead>
              <tbody>
                {commitments.slice(0, 4).map((c, i) => (
                  <tr key={c.id} onClick={() => onOpenCommitment(c.id)} className="clickable-row">
                    <td><div className="task-cell"><div className={`task-icon task-${i % 3}`}><Icon name={i === 0 ? "file" : i === 1 ? "calendar" : "message"} size={17} /></div><div><strong>{c.task}</strong><span>{c.tag || "Personal"} · {c.created || "Recently added"}</span></div></div></td>
                    <td><span className="due-date">{c.deadline ? new Date(c.deadline).toLocaleDateString("en-US", { month: "short", day: "numeric" }) : "No date set"}</span></td>
                    <td><StatusBadge status={c.status || "On track"} /></td>
                    <td><button className="icon-button row-more" aria-label="Open commitment"><Icon name="more" size={17} /></button></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="panel-footer"><span><span className="small-green-dot" /> Showing recent commitments</span><button className="text-button" onClick={() => onOpenCommitment("all")}>Open commitment list <span>→</span></button></div>
        </div>
        <div className="panel attention-panel">
          <div className="panel-header"><div><h2>Needs your attention</h2><p>Review risks before they become surprises.</p></div><span className="alert-count">{riskCount}</span></div>
          {riskCount ? commitments.filter(c => c.status === "At risk").slice(0, 2).map(c => (
            <button className="risk-card" key={c.id} onClick={() => onOpenCommitment(c.id)}>
              <div className="risk-card-top"><span className="risk-icon"><Icon name="alert" size={17} /></span><Badge tone="warning">Deadline risk</Badge><Icon name="arrowUp" size={14} /></div>
              <strong>{c.task}</strong><p>Review the source statement and confirm the latest deadline before acting.</p>
              <div className="risk-card-bottom"><Icon name="clock" size={14} /> Due {c.deadline ? new Date(c.deadline).toLocaleDateString("en-US", { month: "short", day: "numeric" }) : "date not set"}</div>
            </button>
          )) : <div className="empty-state"><Icon name="checkCircle" size={26} /><strong>You're all caught up</strong><span>No risks need your attention.</span></div>}
          <div className="attention-note"><Icon name="shield" size={16} /><span>Alerts are suggestions. Always review the evidence before changing a commitment.</span></div>
        </div>
      </section>
      <section className="bottom-grid">
        <div className="panel activity-panel">
          <div className="panel-header"><div><h2>Agent activity</h2><p>A transparent view of what the workflow has done.</p></div><button className="text-button" onClick={() => onOpenCommitment("activity")}>View log <span>→</span></button></div>
          <div className="activity-list">
            {activity.slice(0, 3).map((item, i) => (
              <div className="activity-item" key={i}><div className={`activity-icon activity-${item.icon}`}><Icon name={item.icon} size={16} /></div><div className="activity-copy"><strong>{item.title}</strong><span>{item.detail}</span></div><time>{item.time}</time></div>
            ))}
          </div>
        </div>
        <div className="panel voice-panel">
          <div className="voice-orbit"><div className="orbit-ring ring-one" /><div className="orbit-ring ring-two" /><div className="mic-circle"><Icon name="voice" size={23} /></div><span className="orbit-dot dot-one" /><span className="orbit-dot dot-two" /><span className="orbit-dot dot-three" /></div>
          <div className="voice-copy"><span className="mini-label">VOICE INBOX</span><h2>It starts with a conversation.</h2><p>Capture a promise naturally. Commitment Radar helps keep it from slipping through the cracks.</p><button className="btn btn-dark" onClick={onShowIngest}><Icon name="voice" size={16} /> Try transcript input</button></div>
        </div>
      </section>
      <div className="integration-strip"><div className="integration-heading"><span className="integration-pulse" /> INTEGRATION STATUS</div><div className="integration-item"><span className="integration-logo omi-logo">o</span><div><strong>Omi</strong><small>{apiStatus?.integrations?.omi?.implemented ? "Integrated" : "Setup required"}</small></div><span className={`status-dot ${apiStatus?.integrations?.omi?.implemented ? "live" : ""}`} /></div><div className="integration-item"><span className="integration-logo qdrant-logo">Q</span><div><strong>Qdrant</strong><small>{apiStatus?.integrations?.qdrant?.implemented ? "Connected" : "Setup required"}</small></div><span className={`status-dot ${apiStatus?.integrations?.qdrant?.implemented ? "live" : ""}`} /></div><div className="integration-item"><span className="integration-logo lyzr-logo">L</span><div><strong>Lyzr</strong><small>{apiStatus?.integrations?.lyzr?.implemented ? "Connected" : "Setup required"}</small></div><span className={`status-dot ${apiStatus?.integrations?.lyzr?.implemented ? "live" : ""}`} /></div></div>
    </>
  );
}

function IngestModal({ onClose, onSubmit, busy, error }) {
  const [transcript, setTranscript] = useState("");
  const [source, setSource] = useState("manual");
  return (
    <div className="modal-backdrop" role="presentation" onMouseDown={e => e.target === e.currentTarget && onClose()}>
      <section className="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
        <div className="modal-top"><div className="modal-icon"><Icon name="voice" size={21} /></div><button className="icon-button" onClick={onClose} aria-label="Close"><Icon name="close" /></button></div>
        <span className="mini-label">NEW COMMITMENT</span><h2 id="modal-title">What did you say you'd do?</h2><p>Paste a transcript or enter a short statement. This scaffold uses manual input; live Omi capture is not connected yet.</p>
        <label className="field-label" htmlFor="source">Transcript source</label>
        <select id="source" value={source} onChange={e => setSource(e.target.value)}><option value="manual">Manual / demo input</option><option value="omi" disabled>Omi integration (not connected)</option></select>
        <label className="field-label" htmlFor="transcript">Statement or transcript</label>
        <textarea id="transcript" value={transcript} onChange={e => setTranscript(e.target.value)} placeholder="Example: I'll send Rahul the invoice by Friday." rows={4} />
        {error && <p className="form-error">{error}</p>}
        <div className="modal-footer"><button className="btn btn-ghost" onClick={onClose}>Cancel</button><button className="btn btn-primary" disabled={busy || transcript.trim().length < 3} onClick={() => onSubmit(transcript, source)}>{busy ? "Processing…" : <><Icon name="sparkle" size={16} /> Extract commitment</>}</button></div>
      </section>
    </div>
  );
}

function DetailModal({ commitment, onClose }) {
  if (!commitment) return null;
  return (
    <div className="modal-backdrop" role="presentation" onMouseDown={e => e.target === e.currentTarget && onClose()}>
      <section className="modal detail-modal" role="dialog" aria-modal="true">
        <div className="modal-top"><div className="modal-icon"><Icon name="file" size={21} /></div><button className="icon-button" onClick={onClose}><Icon name="close" /></button></div>
        <span className="mini-label">COMMITMENT DETAILS</span><h2>{commitment.task}</h2>
        <div className="detail-row"><span>Status</span><StatusBadge status={commitment.status || "On track"} /></div>
        <div className="detail-row"><span>Deadline</span><strong>{commitment.deadline ? new Date(commitment.deadline).toLocaleString() : "Not specified"}</strong></div>
        <div className="evidence-box"><span className="evidence-label"><Icon name="file" size={14} /> SOURCE STATEMENT</span><p>“{commitment.source_text}”</p></div>
        <p className="detail-caveat"><Icon name="shield" size={15} /> Evidence shown is the original statement. This scaffold has not run integrated semantic conflict analysis.</p>
        <div className="modal-footer"><button className="btn btn-ghost" onClick={onClose}>Close</button></div>
      </section>
    </div>
  );
}

function SecondaryView({ active, commitments, activity, onShowIngest }) {
  const titles = {
    commitments: ["Commitments", "A clear list of what you've said you'll do."],
    voice: ["Voice inbox", "Transcript review will appear here when Omi is integrated."],
    activity: ["Agent activity", "See the steps the workflow actually executed."],
    settings: ["Settings & integrations", "Manage connected services and privacy controls."]
  };
  const [search, setSearch] = useState("");
  const [demoTranscript, setDemoTranscript] = useState(false);
  const [apiDetails, setApiDetails] = useState(null);
  const title = titles[active] || titles.commitments;
  const visible = commitments.filter(c => (c.task || "").toLowerCase().includes(search.toLowerCase()));
  return (
    <div className="secondary-view">
      <div className="page-heading"><div><div className="eyebrow"><span className="eyebrow-line" /> WORKSPACE</div><h1>{title[0]}</h1><p>{title[1]}</p></div>{active === "commitments" && <button className="btn btn-primary" onClick={onShowIngest}><Icon name="plus" size={17} /> Add commitment</button>}</div>
      {active === "commitments" && <div className="panel secondary-panel"><div className="list-toolbar"><div className="search-box"><Icon name="search" size={17} /><input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search commitments…" /></div><button className="btn btn-ghost"><Icon name="filter" size={16} /> Filters</button></div>{visible.map(c => <div className="secondary-row" key={c.id}><div className="task-icon task-0"><Icon name="file" /></div><div className="secondary-row-main"><strong>{c.task}</strong><span>{c.source_text}</span></div><StatusBadge status={c.status || "On track"} /></div>)}{visible.length === 0 && <div className="empty-state">No commitments match that search.</div>}</div>}
      {active === "voice" && <div className="panel empty-page"><div className="empty-page-icon"><Icon name="voice" size={27} /></div><h2>Voice inbox is ready for integration</h2><p>Connect the supported Omi developer route to populate real transcripts here. Until then, use manual input to test the API scaffold.</p><button className="btn btn-primary" onClick={onShowIngest}>Try manual transcript input</button></div>}
      {active === "activity" && <div className="panel secondary-panel">{activity.map((a, i) => <div className="activity-item activity-item-large" key={i}><div className="activity-icon activity-agent"><Icon name={a.icon} /></div><div className="activity-copy"><strong>{a.title}</strong><span>{a.detail}</span></div><time>{a.time}</time></div>)}</div>}
      {active === "settings" && <div className="settings-grid"><div className="panel setting-card"><div className="setting-icon"><Icon name="voice" /></div><h2>Omi voice capture</h2><p>Connect a supported Omi capture/webhook route. Verify authentication and event schema before enabling.</p><Badge tone="warning">Not connected</Badge></div><div className="panel setting-card"><div className="setting-icon"><Icon name="database" /></div><h2>Qdrant memory</h2><p>Configure the cloud URL, key, collection and a real embedding model for persistent semantic retrieval.</p><Badge tone="warning">Adapter pending</Badge></div><div className="panel setting-card"><div className="setting-icon"><Icon name="agent" /></div><h2>Lyzr agents</h2><p>Configure a supported Lyzr agent API call and validate its response before showing execution logs.</p><Badge tone="warning">Adapter pending</Badge></div><div className="panel setting-card"><div className="setting-icon"><Icon name="shield" /></div><h2>Privacy controls</h2><p>Deletion is currently local to the in-memory demo store. Persistent deletion and multi-user access controls are not implemented.</p><Badge tone="neutral">Scaffold</Badge></div></div>}
    </div>
  );
}

export default function App() {
  const [active, setActive] = useState("overview");
  const [commitments, setCommitments] = useState(initialCommitments);
  const [activity, setActivity] = useState(initialActivity);
  const [apiStatus, setApiStatus] = useState(null);
  const [showIngest, setShowIngest] = useState(false);
  const [selected, setSelected] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API_BASE}/health`).then(r => r.ok ? r.json() : Promise.reject()).then(setApiStatus).catch(() => setApiStatus(null));
    fetch(`${API_BASE}/api/commitments`).then(r => r.ok ? r.json() : Promise.reject()).then(items => {
      if (items.length) setCommitments(items.map(c => ({ ...c, status: c.status === "open" ? "On track" : c.status, created: new Date(c.created_at).toLocaleString(), tag: c.source || "Manual" })));
    }).catch(() => {});
  }, []);

  const openCommitment = id => {
    if (id === "all") setActive("commitments");
    else if (id === "activity") setActive("activity");
    else {
      const found = commitments.find(c => c.id === id);
      if (found) setSelected(found);
    }
  };

  async function submitTranscript(transcript, source) {
    setBusy(true); setError("");
    try {
      const response = await fetch(`${API_BASE}/api/ingest`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ transcript, source })
      });
      if (!response.ok) throw new Error(`API returned ${response.status}. Is the backend running?`);
      const data = await response.json();
      const item = { ...data.commitment, status: data.conflict_detected ? "At risk" : "On track", created: "Just now", tag: source === "omi" ? "Omi" : "Manual" };
      setCommitments(prev => [item, ...prev.filter(c => c.id !== item.id)]);
      setActivity(prev => [
        { icon: "agent", title: "Transcript processed (scaffold)", detail: data.explanation, time: "Just now" },
        ...prev
      ]);
      setShowIngest(false);
      setSelected(item);
    } catch (e) {
      setError(`${e.message} Start the FastAPI server and check VITE_API_BASE_URL.`);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="app-shell">
      <Sidebar active={active} setActive={setActive} />
      <main className="main-content">
        <header className="topbar"><div className="breadcrumbs"><span>Workspace</span><span className="crumb-slash">/</span><strong>{active === "overview" ? "Overview" : active.charAt(0).toUpperCase() + active.slice(1)}</strong></div><div className="topbar-actions"><div className="search-global"><Icon name="search" size={16} /><span>Search anything</span><kbd>⌘ K</kbd></div><button className="icon-button notification-button" aria-label="Notifications"><Icon name="bell" size={19} /><i /></button><div className="avatar avatar-indigo top-avatar">AY</div></div></header>
        <div className="page-container">
          {active === "overview"
            ? <Overview commitments={commitments} activity={activity} onOpenCommitment={openCommitment} onShowIngest={() => { setError(""); setShowIngest(true); }} apiStatus={apiStatus} />
            : <SecondaryView active={active} commitments={commitments} activity={activity} onShowIngest={() => { setError(""); setShowIngest(true); }} />}
          <footer className="app-footer"><span>© 2026 Commitment Radar</span><span><span className="footer-status-dot" /> Local scaffold · integrations pending</span><button><Icon name="help" size={14} /> Help & docs</button></footer>
        </div>
      </main>
      {showIngest && <IngestModal onClose={() => setShowIngest(false)} onSubmit={submitTranscript} busy={busy} error={error} />}
      {selected && <DetailModal commitment={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
