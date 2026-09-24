import React, { useState } from "react";

import {
  Leaf,
  Send,
  Settings2,
  Activity,
  Database,
  Network,
  ShieldCheck,
  MapPin,
  RefreshCw,
  Sparkles,
} from "lucide-react";

import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  Handle,
  Position,
} from "@xyflow/react";

import "@xyflow/react/dist/style.css";

const API =
  import.meta.env.VITE_API_URL || "http://localhost:8000";

/* =========================================================
   INITIAL ENVIRONMENTAL METRICS
========================================================= */

const initialMetrics = {
  soil_organic_carbon: 0.3,
  soil_ph: 7,
  soil_moisture: "low",
  rainfall: "low",
  temperature: 25,
  land_use_type: "monoculture",
  crop: "wheat",
  region: "semi-arid",
  pollution: "low",
  deforestation: "low",
  species_richness: 35,
  habitat_diversity: 50,
};

/* =========================================================
   METRIC CARD
========================================================= */

function Metric({ label, value, unit, accent }) {
  return (
    <div className="glass rounded-2xl p-4">
      <div className="text-xs text-slate-400 mb-2">
        {label}
      </div>

      <div className="flex items-end gap-1">
        <span
          className={`text-2xl font-semibold ${
            accent || "text-white"
          }`}
        >
          {value}
        </span>

        {unit && (
          <span className="text-xs text-slate-400 mb-1">
            {unit}
          </span>
        )}
      </div>
    </div>
  );
}

/* =========================================================
   CUSTOM REASONING NODE
========================================================= */

function ReasoningNode({
  data,
  variant = "default",
}) {
  const styles = {
    environment:
      "border-slate-700/80 bg-slate-900/95",

    land:
      "border-amber-400/30 bg-slate-900/95",

    mechanism:
      "border-blue-400/30 bg-slate-900/95",

    intervention:
      "border-emerald-400/60 bg-emerald-950/70 shadow-[0_0_30px_rgba(52,211,153,0.12)]",

    outcome:
      "border-purple-400/40 bg-slate-900/95 shadow-[0_0_30px_rgba(168,85,247,0.10)]",
  };

  return (
    <div
      className={`
        relative
        w-[250px]
        min-h-[92px]
        rounded-2xl
        border
        px-5
        py-4
        shadow-xl
        backdrop-blur-xl
        ${styles[variant] || styles.environment}
      `}
    >
      {/* TARGET HANDLE */}

      <Handle
        type="target"
        position={Position.Top}
        className="!h-2.5 !w-2.5 !border-2 !border-slate-900 !bg-slate-300"
      />

      {/* CATEGORY */}

      {data.category && (
        <div
          className={`text-[10px] uppercase tracking-[0.18em] mb-2 ${
            variant === "intervention"
              ? "text-emerald-400"
              : variant === "outcome"
              ? "text-purple-300"
              : "text-slate-500"
          }`}
        >
          {data.category}
        </div>
      )}

      {/* NODE CONTENT */}

      <div className="flex items-start gap-3">
        <div className="text-2xl leading-none shrink-0">
          {data.icon}
        </div>

        <div className="min-w-0">
          <div className="text-sm font-semibold text-slate-100 leading-snug">
            {data.label}
          </div>

          {data.description && (
            <div className="text-[11px] text-slate-500 mt-1 leading-relaxed">
              {data.description}
            </div>
          )}
        </div>
      </div>

      {/* SOURCE HANDLE */}

      <Handle
        type="source"
        position={Position.Bottom}
        className="!h-2.5 !w-2.5 !border-2 !border-slate-900 !bg-slate-300"
      />
    </div>
  );
}

const nodeTypes = {
  reasoning: ReasoningNode,
};

/* =========================================================
   REASONING GRAPH
========================================================= */

function Graph({ metrics }) {
  const nodes = [
    {
      id: "rain",
      type: "reasoning",
      position: { x: 20, y: 60 },
      data: {
        category: "Environmental condition",
        icon: "🌧️",
        label: `Rainfall · ${metrics.rainfall}`,
        description: "Water availability constraint",
      },
    },

    {
      id: "moist",
      type: "reasoning",
      position: { x: 325, y: 60 },
      data: {
        category: "Environmental condition",
        icon: "💧",
        label: `Soil moisture · ${metrics.soil_moisture}`,
        description: "Soil water availability",
      },
    },

    {
      id: "carbon",
      type: "reasoning",
      position: { x: 630, y: 60 },
      data: {
        category: "Soil condition",
        icon: "🌱",
        label: `Soil organic carbon · ${metrics.soil_organic_carbon}%`,
        description: "Organic matter and carbon inputs",
      },
    },

    {
      id: "land",
      type: "reasoning",
      position: { x: 20, y: 260 },
      data: {
        category: "Land use",
        icon: "🌾",
        label: `${metrics.land_use_type || "Monoculture"} ${
          metrics.crop || "crop"
        }`,
        description: "Current agricultural system",
      },
    },

    {
      id: "action",
      type: "reasoning",
      position: { x: 630, y: 260 },
      data: {
        category: "Intervention",
        icon: "🌳",
        label: "Agroforestry / intercropping",
        description: "Increase structural and habitat diversity",
      },
    },

    {
      id: "habitat",
      type: "reasoning",
      position: { x: 325, y: 405 },
      data: {
        category: "Ecological mechanism",
        icon: "🦋",
        label: "Habitat diversity",
        description: "More habitat structure and ecological niches",
      },
    },

    {
      id: "richness",
      type: "reasoning",
      position: { x: 325, y: 555 },
      data: {
        category: "Biodiversity outcome",
        icon: "🧬",
        label: `Species richness · ${metrics.species_richness}`,
        description: "Biodiversity response",
      },
    },
  ];

  const edges = [
    {
      id: "rain-moist",
      source: "rain",
      target: "moist",
      type: "smoothstep",
      animated: false,
      style: {
        stroke: "#64748b",
        strokeWidth: 1.5,
      },
    },

    {
      id: "moist-carbon",
      source: "moist",
      target: "carbon",
      type: "smoothstep",
      animated: false,
      style: {
        stroke: "#64748b",
        strokeWidth: 1.5,
      },
    },

    {
      id: "land-habitat",
      source: "land",
      target: "habitat",
      type: "smoothstep",
      animated: false,
      style: {
        stroke: "#a78bfa",
        strokeWidth: 1.8,
      },
    },

    {
      id: "carbon-habitat",
      source: "carbon",
      target: "habitat",
      type: "smoothstep",
      animated: false,
      style: {
        stroke: "#60a5fa",
        strokeWidth: 1.8,
      },
    },

    {
      id: "action-habitat",
      source: "action",
      target: "habitat",
      type: "smoothstep",
      animated: true,
      style: {
        stroke: "#34d399",
        strokeWidth: 2.2,
      },
    },

    {
      id: "habitat-richness",
      source: "habitat",
      target: "richness",
      type: "smoothstep",
      animated: true,
      style: {
        stroke: "#c084fc",
        strokeWidth: 2,
      },
    },
  ];

  return (
    <div className="h-[700px] rounded-3xl overflow-hidden border border-white/10 bg-[#020617] shadow-2xl">

      {/* GRAPH HEADER */}

      <div className="absolute z-10 pointer-events-none p-5">
        <div className="rounded-xl border border-white/10 bg-slate-950/80 backdrop-blur-xl px-4 py-3">
          <div className="text-xs font-medium text-slate-300">
            Causal reasoning backbone
          </div>

          <div className="text-[11px] text-slate-500 mt-1">
            Environmental conditions → ecological mechanisms → biodiversity
          </div>
        </div>
      </div>

      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        fitView
        fitViewOptions={{
          padding: 0.15,
          minZoom: 0.65,
          maxZoom: 1.1,
        }}
        minZoom={0.45}
        maxZoom={1.5}
        nodesDraggable={true}
        nodesConnectable={false}
        elementsSelectable={true}
        proOptions={{
          hideAttribution: false,
        }}
      >
        <Background
          variant="dots"
          gap={28}
          size={1}
          color="#334155"
        />

        <Controls
          showInteractive={false}
        />

        <MiniMap
          pannable
          zoomable
          nodeColor={(node) => {
            if (node.id === "action") {
              return "#34d399";
            }

            if (node.id === "richness") {
              return "#c084fc";
            }

            if (node.id === "habitat") {
              return "#60a5fa";
            }

            return "#475569";
          }}
        />
      </ReactFlow>
    </div>
  );
}

/* =========================================================
   EVIDENCE
========================================================= */

function Evidence({ evidence }) {
  if (!Array.isArray(evidence) || evidence.length === 0) {
    return null;
  }

  const uniqueEvidence = [];
  const seen = new Set();

  evidence.forEach((item) => {
    if (!item) return;

    const key = [
      item.source_title || "",
      item.source_url || "",
      item.page_number ?? "",
    ].join("|");

    if (!seen.has(key)) {
      seen.add(key);
      uniqueEvidence.push(item);
    }
  });

  if (uniqueEvidence.length === 0) {
    return null;
  }

  return (
    <div className="mt-5 space-y-3">

      <div className="flex items-center gap-2 text-xs text-slate-400">
        <span className="text-emerald-400">▸</span>
        <span>Evidence</span>
      </div>

      {uniqueEvidence.map((item, index) => (
        <div
          key={`${item.source_title || "source"}-${index}`}
          className="rounded-xl border border-white/10 bg-white/[0.03] p-4"
        >
          <div className="flex items-start justify-between gap-3">

            <div className="text-sm font-medium text-white">
              {item.source_title || "Source"}
            </div>

            {item.page_number !== null &&
              item.page_number !== undefined && (
                <span className="shrink-0 rounded-lg bg-white/5 px-2 py-1 text-[11px] text-slate-400">
                  Page {item.page_number}
                </span>
              )}

          </div>

          {item.source_url && (
            <a
              href={item.source_url}
              target="_blank"
              rel="noreferrer"
              className="inline-block mt-2 text-xs text-emerald-400 hover:text-emerald-300"
            >
              Open source
            </a>
          )}

          {item.supporting_excerpt_or_summary && (
            <div className="mt-3 rounded-lg bg-black/20 p-3">
              <p className="text-xs text-slate-400 leading-relaxed">
                {item.supporting_excerpt_or_summary}
              </p>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

/* =========================================================
   RETRIEVED SOURCES
========================================================= */

function RetrievedSources({ sources }) {
  if (!Array.isArray(sources) || sources.length === 0) {
    return null;
  }

  const grouped = {};

  sources.forEach((source) => {
    if (!source) return;

    const title =
      source.source_title ||
      source.title ||
      "Unknown source";

    const url =
      source.source_url ||
      source.url ||
      "";

    const key = `${title}|${url}`;

    if (!grouped[key]) {
      grouped[key] = {
        source_title: title,
        source_url: url,
        pages: new Set(),
      };
    }

    const page =
      source.page_number ??
      source.page ??
      null;

    if (page !== null && page !== undefined) {
      grouped[key].pages.add(page);
    }
  });

  const groupedSources = Object.values(grouped);

  return (
    <div className="mt-5">

      <div className="flex items-center gap-2 text-xs text-slate-400 mb-3">
        <span className="text-emerald-400">▸</span>
        <span>Retrieved sources</span>
      </div>

      <div className="space-y-2">

        {groupedSources.map((source, index) => {
          const pages = Array.from(source.pages).sort(
            (a, b) => Number(a) - Number(b)
          );

          return (
            <div
              key={`${source.source_title}-${index}`}
              className="rounded-xl border border-white/10 bg-white/[0.02] p-3"
            >
              <div className="text-xs text-slate-300">
                {source.source_title}
              </div>

              {source.source_url && (
                <a
                  href={source.source_url}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-block mt-1 text-xs text-emerald-400 hover:text-emerald-300"
                >
                  Open source
                </a>
              )}

              {pages.length > 0 && (
                <div className="mt-2 text-[11px] text-slate-500">
                  Retrieved pages:{" "}
                  {pages.slice(0, 12).join(", ")}

                  {pages.length > 12 &&
                    ` +${pages.length - 12} more`}
                </div>
              )}
            </div>
          );
        })}

      </div>
    </div>
  );
}

/* =========================================================
   ASSISTANT RESPONSE
========================================================= */

function AssistantResponse({ data }) {
  if (!data) return null;

  /* ---------------- Clarification ---------------- */

  if (data.type === "clarification") {
    return (
      <div className="rounded-2xl border border-yellow-400/20 bg-yellow-400/5 p-4">

        <div className="flex items-center gap-2 text-yellow-300 font-medium mb-2">
          <Sparkles size={16} />
          <span>More information needed</span>
        </div>

        <p className="text-sm text-slate-300">
          {data.question}
        </p>

        {Array.isArray(data.missing_metrics) &&
          data.missing_metrics.length > 0 && (
            <div className="mt-3 flex flex-wrap gap-2">

              {data.missing_metrics.map((metric) => (
                <span
                  key={metric}
                  className="px-2 py-1 rounded-lg bg-yellow-400/10 text-xs text-yellow-300"
                >
                  {metric}
                </span>
              ))}

            </div>
          )}

      </div>
    );
  }

  /* ---------------- Error ---------------- */

  if (data.type === "error") {
    return (
      <div className="rounded-2xl border border-red-400/20 bg-red-400/5 p-4">

        <p className="text-sm text-red-300">
          {data.question ||
            data.message ||
            "Something went wrong."}
        </p>

      </div>
    );
  }

  /* ---------------- Recommendations ---------------- */

  const recommendations =
    Array.isArray(data.recommendations)
      ? data.recommendations
      : [];

  return (
    <div className="space-y-4">

      {/* SUMMARY */}

      {data.summary && (
        <div className="text-sm text-slate-300 leading-relaxed">
          {data.summary}
        </div>
      )}

      {/* RECOMMENDATIONS */}

      {recommendations.map((rec, index) => (
        <div
          key={index}
          className="rounded-2xl border border-white/10 bg-white/[0.03] p-5"
        >

          <div className="flex items-start justify-between gap-4">

            <div>

              <div className="text-xs text-emerald-400 mb-1">
                Recommendation{" "}
                {String(index + 1).padStart(2, "0")}
              </div>

              <h3 className="text-base font-semibold text-white">
                {rec.what_to_do ||
                  "Recommendation"}
              </h3>

            </div>

            <span className="shrink-0 rounded-full bg-white/5 px-3 py-1 text-xs text-slate-300">
              {rec.confidence || "unknown"} confidence
            </span>

          </div>

          {/* WHY IT WORKS */}

          {rec.why_it_works && (
            <p className="mt-3 text-sm text-slate-400 leading-relaxed">
              {rec.why_it_works}
            </p>
          )}

          {/* CAUSAL CHAIN */}

          {Array.isArray(rec.causal_chain) &&
            rec.causal_chain.length > 0 && (

              <div className="mt-4">

                <div className="text-xs text-slate-500 mb-2">
                  Causal chain
                </div>

                <div className="flex flex-wrap items-center gap-2">

                  {rec.causal_chain.map(
                    (item, chainIndex) => (

                      <React.Fragment key={chainIndex}>

                        <span className="rounded-lg bg-emerald-400/10 px-2 py-1 text-xs text-emerald-300 break-words">
                          {item}
                        </span>

                        {chainIndex <
                          rec.causal_chain.length - 1 && (

                          <span
                            className="text-slate-500 px-1 text-sm"
                            aria-hidden="true"
                          >
                            →
                          </span>

                        )}

                      </React.Fragment>

                    )
                  )}

                </div>

              </div>

            )}

          {/* IMPACTED METRICS */}

          {Array.isArray(rec.impacted_metrics) &&
            rec.impacted_metrics.length > 0 && (

              <div className="mt-4 flex flex-wrap gap-2">

                {rec.impacted_metrics.map(
                  (metric, metricIndex) => (

                    <span
                      key={`${metric}-${metricIndex}`}
                      className="text-xs text-slate-300 bg-white/5 rounded-lg px-2 py-1"
                    >
                      ↑ {metric}
                    </span>

                  )
                )}

              </div>

            )}

          {/* TIME HORIZON */}

          {rec.time_horizon && (
            <div className="mt-4 text-xs text-slate-500">

              Time horizon:{" "}

              <span className="text-slate-300">
                {rec.time_horizon}
              </span>

            </div>
          )}

          {/* EVIDENCE */}

          <Evidence evidence={rec.evidence} />

        </div>
      ))}

      {/* RETRIEVED SOURCES */}

      <RetrievedSources
        sources={data.retrieved_sources}
      />

    </div>
  );
}

/* =========================================================
   MAIN APP
========================================================= */

function App() {
  const [tab, setTab] = useState("Scientist");

  const [metrics, setMetrics] =
    useState(initialMetrics);

  const [message, setMessage] = useState("");

  const [loading, setLoading] = useState(false);

  const [history, setHistory] = useState([]);

  const [session] = useState(() =>
    crypto.randomUUID()
  );

  /* =======================================================
     ASK BACKEND
  ======================================================= */

  const ask = async () => {
    if (!message.trim() || loading) return;

    const currentMessage = message.trim();

    setLoading(true);

    try {
      const response = await fetch(`${API}/chat`, {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          session_id: session,
          message: currentMessage,
          metrics,
        }),
      });

      if (!response.ok) {
        throw new Error(
          `HTTP ${response.status}`
        );
      }

      const data = await response.json();

      setHistory((previousHistory) => [
        ...previousHistory,
        {
          q: currentMessage,
          a: data,
        },
      ]);

      setMessage("");

    } catch (error) {
      console.error(error);

      setHistory((previousHistory) => [
        ...previousHistory,
        {
          q: currentMessage,
          a: {
            type: "error",
            question:
              "Could not reach FastAPI. Start the backend on port 8000.",
          },
        },
      ]);

    } finally {
      setLoading(false);
    }
  };

  /* =======================================================
     ENTER KEY
  ======================================================= */

  const handleKeyDown = (event) => {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();
      ask();
    }
  };

  /* =======================================================
     UPDATE METRIC
  ======================================================= */

  const updateMetric = (key, value) => {
    setMetrics((previous) => ({
      ...previous,
      [key]: value,
    }));
  };

  /* =======================================================
     UI
  ======================================================= */

  return (
    <div className="min-h-screen bg-[#07110d] text-white">

      {/* ===================================================
          HEADER
      =================================================== */}

      <header className="border-b border-white/10 bg-black/20 backdrop-blur-xl">

        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">

          <div className="flex items-center gap-3">

            <div className="h-10 w-10 rounded-xl bg-emerald-400/10 flex items-center justify-center">

              <Leaf
                size={22}
                className="text-emerald-400"
              />

            </div>

            <div>

              <div className="font-semibold">
                Darukaa.Earth
              </div>

              <div className="text-xs text-slate-500">
                AI Biodiversity Intelligence
              </div>

            </div>

          </div>

          <div className="flex items-center gap-2 text-xs text-emerald-400">

            <div className="h-2 w-2 rounded-full bg-emerald-400" />

            System Online

          </div>

        </div>

      </header>

      {/* ===================================================
          TABS
      =================================================== */}

      <div className="max-w-7xl mx-auto px-6 pt-6">

        <div className="flex gap-2 overflow-x-auto">

          {[
            {
              name: "Scientist",
              icon: Sparkles,
            },
            {
              name: "Environmental Profile",
              icon: Activity,
            },
            {
              name: "Reasoning",
              icon: Network,
            },
          ].map((item) => {

            const Icon = item.icon;

            const active =
              tab === item.name;

            return (
              <button
                key={item.name}
                onClick={() =>
                  setTab(item.name)
                }
                className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm transition ${
                  active
                    ? "bg-emerald-400/10 text-emerald-300 border border-emerald-400/20"
                    : "text-slate-400 hover:text-white hover:bg-white/5"
                }`}
              >
                <Icon size={15} />
                {item.name}
              </button>
            );
          })}

        </div>

      </div>

      {/* ===================================================
          CONTENT
      =================================================== */}

      <main className="max-w-7xl mx-auto px-6 py-6">

        {/* =================================================
            SCIENTIST TAB
        ================================================= */}

        {tab === "Scientist" && (

          <div className="grid lg:grid-cols-[1fr_350px] gap-6">

            {/* CHAT */}

            <section className="glass rounded-3xl border border-white/10 overflow-hidden">

              <div className="px-6 py-5 border-b border-white/10 flex items-center justify-between">

                <div>

                  <h1 className="font-semibold">
                    Environmental Scientist
                  </h1>

                  <p className="text-xs text-slate-500 mt-1">
                    Evidence-grounded biodiversity reasoning
                  </p>

                </div>

                <div className="flex items-center gap-2 text-xs text-slate-500">

                  <ShieldCheck size={14} />

                  Grounded AI

                </div>

              </div>

              {/* CHAT HISTORY */}

              <div className="p-6 space-y-6 min-h-[520px]">

                {history.length === 0 && (

                  <div className="h-[450px] flex flex-col items-center justify-center text-center">

                    <div className="h-16 w-16 rounded-2xl bg-emerald-400/10 flex items-center justify-center mb-5">

                      <Leaf
                        size={30}
                        className="text-emerald-400"
                      />

                    </div>

                    <h2 className="text-xl font-semibold">
                      Ask about your environment
                    </h2>

                    <p className="text-sm text-slate-500 max-w-md mt-2">
                      Ask for biodiversity recommendations,
                      soil-management advice, or environmental
                      reasoning based on the supplied metrics.
                    </p>

                  </div>

                )}

                {/* EVERY QUESTION + ANSWER */}

                {history.map((item, index) => (

                  <div
                    key={index}
                    className="space-y-4"
                  >

                    {/* USER */}

                    <div className="flex justify-end">

                      <div className="max-w-[80%]">

                        <div className="text-xs text-slate-500 mb-1 text-right">
                          You
                        </div>

                        <div className="rounded-2xl rounded-tr-md bg-emerald-400/10 border border-emerald-400/10 px-4 py-3 text-sm text-emerald-50">
                          {item.q}
                        </div>

                      </div>

                    </div>

                    {/* ASSISTANT */}

                    <div className="flex justify-start">

                      <div className="max-w-[90%] w-full">

                        <div className="text-xs text-slate-500 mb-1">
                          Darukaa Scientist
                        </div>

                        <div className="rounded-2xl rounded-tl-md bg-white/[0.025] border border-white/10 p-4">

                          <AssistantResponse
                            data={item.a}
                          />

                        </div>

                      </div>

                    </div>

                  </div>

                ))}

                {/* LOADING */}

                {loading && (

                  <div className="flex justify-start">

                    <div className="rounded-2xl bg-white/[0.03] border border-white/10 px-4 py-3">

                      <div className="flex items-center gap-3 text-sm text-slate-400">

                        <RefreshCw
                          size={15}
                          className="animate-spin"
                        />

                        Analyzing environmental evidence...

                      </div>

                    </div>

                  </div>

                )}

              </div>

              {/* INPUT */}

              <div className="border-t border-white/10 p-5">

                <div className="flex items-end gap-3">

                  <textarea
                    value={message}
                    onChange={(e) =>
                      setMessage(e.target.value)
                    }
                    onKeyDown={handleKeyDown}
                    placeholder="Ask a biodiversity question..."
                    rows={2}
                    className="flex-1 resize-none rounded-2xl bg-white/[0.04] border border-white/10 px-4 py-3 text-sm text-white placeholder:text-slate-600 outline-none focus:border-emerald-400/30"
                  />

                  <button
                    onClick={ask}
                    disabled={
                      loading ||
                      !message.trim()
                    }
                    className="h-12 w-12 rounded-2xl bg-emerald-400 text-black flex items-center justify-center disabled:opacity-30 disabled:cursor-not-allowed hover:bg-emerald-300 transition"
                  >

                    <Send size={18} />

                  </button>

                </div>

                <div className="text-[11px] text-slate-600 mt-2">
                  Press Enter to send · Shift + Enter for
                  new line
                </div>

              </div>

            </section>

            {/* SIDE PANEL */}

            <aside className="space-y-4">

              {/* CURRENT ENVIRONMENT */}

              <div className="glass rounded-3xl border border-white/10 p-5">

                <div className="flex items-center gap-2 mb-4">

                  <Activity
                    size={17}
                    className="text-emerald-400"
                  />

                  <h2 className="font-medium">
                    Current Environment
                  </h2>

                </div>

                <div className="grid grid-cols-2 gap-3">

                  <Metric
                    label="Soil pH"
                    value={metrics.soil_ph}
                  />

                  <Metric
                    label="Organic Carbon"
                    value={
                      metrics.soil_organic_carbon
                    }
                    unit="%"
                    accent="text-emerald-300"
                  />

                  <Metric
                    label="Species Richness"
                    value={
                      metrics.species_richness
                    }
                  />

                  <Metric
                    label="Habitat Diversity"
                    value={
                      metrics.habitat_diversity
                    }
                  />

                  <Metric
                    label="Temperature"
                    value={metrics.temperature}
                    unit="°C"
                  />

                  <Metric
                    label="Rainfall"
                    value={metrics.rainfall}
                  />

                </div>

              </div>

              {/* REGION */}

              <div className="glass rounded-3xl border border-white/10 p-5">

                <div className="flex items-center gap-2 mb-3">

                  <MapPin
                    size={16}
                    className="text-emerald-400"
                  />

                  <span className="text-sm font-medium">
                    Region
                  </span>

                </div>

                <div className="text-sm text-slate-300">
                  {metrics.region}
                </div>

              </div>

              {/* EVIDENCE LAYER */}

              <div className="glass rounded-3xl border border-white/10 p-5">

                <div className="flex items-center gap-2 mb-3">

                  <Database
                    size={16}
                    className="text-emerald-400"
                  />

                  <span className="text-sm font-medium">
                    Evidence Layer
                  </span>

                </div>

                <p className="text-xs text-slate-500 leading-relaxed">
                  Recommendations are generated using
                  retrieved environmental evidence and a
                  causal reasoning graph.
                </p>

              </div>

            </aside>

          </div>

        )}

        {/* =================================================
            ENVIRONMENTAL PROFILE
        ================================================= */}

        {tab === "Environmental Profile" && (

          <div className="glass rounded-3xl border border-white/10 p-6">

            <div className="flex items-center justify-between mb-6">

              <div>

                <h1 className="text-xl font-semibold">
                  Environmental Profile
                </h1>

                <p className="text-sm text-slate-500 mt-1">
                  Current environmental inputs used by the
                  reasoning system.
                </p>

              </div>

              <Settings2
                size={20}
                className="text-slate-500"
              />

            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">

              {Object.entries(metrics).map(
                ([key, value]) => (

                  <div
                    key={key}
                    className="rounded-2xl border border-white/10 bg-white/[0.03] p-4"
                  >

                    <div className="text-xs text-slate-500 mb-2">
                      {key.replaceAll("_", " ")}
                    </div>

                    <input
                      value={value ?? ""}
                      onChange={(e) =>
                        updateMetric(
                          key,
                          e.target.value
                        )
                      }
                      className="w-full bg-transparent text-white text-sm outline-none"
                    />

                  </div>

                )
              )}

            </div>

          </div>

        )}

        {/* =================================================
            REASONING TAB
        ================================================= */}

        {tab === "Reasoning" && (

          <div className="space-y-5">

            <div>

              <h1 className="text-xl font-semibold">
                Causal Reasoning Graph
              </h1>

              <p className="text-sm text-slate-500 mt-1">
                Environmental relationships used as the
                reasoning backbone.
              </p>

            </div>

            <Graph metrics={metrics} />

          </div>

        )}

      </main>

    </div>
  );
}

export default App;