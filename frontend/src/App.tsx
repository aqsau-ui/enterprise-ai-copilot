import {
  useState,
  type KeyboardEvent,
} from "react";

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  ScatterChart,
  Scatter,
} from "recharts";

import "./App.css";


/* ============================================================
   TYPES
============================================================ */

type Mode =
  | "document"
  | "web"
  | "data";


type Source = {
  source: string;
  page: number;
  score: number;
  faiss_score?: number;
  bm25_score?: number;
};


type VisualizationPoint = {
  label?: string;
  value?: number;
  x?: number;
  y?: number;
};


type Visualization = {
  type:
    | "bar"
    | "pie"
    | "scatter";

  title: string;

  xKey: string;

  yKey: string;

  xLabel?: string;

  yLabel?: string;

  data: VisualizationPoint[];
};


type Message = {
  id: number;

  role:
    | "user"
    | "assistant";

  mode?: Mode;

  content: string;

  sources?: Source[];

  visualization?: Visualization;
};


/* ============================================================
   PIE COLORS
============================================================ */

const PIE_COLORS = [
  "#8b5cf6",
  "#22d3ee",
  "#34d399",
  "#f59e0b",
  "#f472b6",
  "#60a5fa",
];


/* ============================================================
   DATA VISUALIZATION
============================================================ */

function DataVisualization({
  visualization,
}: {
  visualization: Visualization;
}) {

  if (
    !visualization ||
    !visualization.data ||
    visualization.data.length === 0
  ) {
    return null;
  }


  /* ==========================================================
     PIE
  ========================================================== */

  if (
    visualization.type === "pie"
  ) {

    return (
      <div className="data-visualization">

        <div className="visualization-header">

          <div>

            <div className="visualization-eyebrow">
              DATA VISUALIZATION
            </div>

            <h3>
              {visualization.title}
            </h3>

          </div>

          <span className="visualization-badge">
            PIE
          </span>

        </div>


        <div
          className="chart-container"
          style={{
            width: "100%",
            height: 320,
          }}
        >

          <ResponsiveContainer
            width="100%"
            height="100%"
          >

            <PieChart>

              <Pie
                data={
                  visualization.data
                }
                dataKey="value"
                nameKey="label"
                cx="50%"
                cy="45%"
                outerRadius={105}
                innerRadius={55}
                paddingAngle={3}
              >

                {visualization.data.map(
                  (_, index) => (
                    <Cell
                      key={index}
                      fill={
                        PIE_COLORS[
                          index %
                            PIE_COLORS.length
                        ]
                      }
                    />
                  )
                )}

              </Pie>

              <Tooltip
                contentStyle={{
                  background:
                    "#11121d",
                  border:
                    "1px solid #2b2d42",
                  borderRadius:
                    "12px",
                  color:
                    "#ffffff",
                }}
              />

            </PieChart>

          </ResponsiveContainer>

        </div>


        <div className="chart-legend">

          {visualization.data.map(
            (item, index) => (

              <div
                className="chart-legend-item"
                key={`${item.label}-${index}`}
              >

                <span
                  className="legend-dot"
                  style={{
                    background:
                      PIE_COLORS[
                        index %
                          PIE_COLORS.length
                      ],
                  }}
                />

                <span>
                  {item.label}
                </span>

                <strong>
                  {item.value}
                </strong>

              </div>

            )
          )}

        </div>

      </div>
    );
  }


  /* ==========================================================
     BAR
  ========================================================== */

  if (
    visualization.type === "bar"
  ) {

    return (
      <div className="data-visualization">

        <div className="visualization-header">

          <div>

            <div className="visualization-eyebrow">
              DATA VISUALIZATION
            </div>

            <h3>
              {visualization.title}
            </h3>

          </div>

          <span className="visualization-badge">
            BAR
          </span>

        </div>


        <div
          className="chart-container"
          style={{
            width: "100%",
            height: 320,
          }}
        >

          <ResponsiveContainer
            width="100%"
            height="100%"
          >

            <BarChart
              data={
                visualization.data
              }
              margin={{
                top: 10,
                right: 15,
                left: 0,
                bottom: 10,
              }}
            >

              <CartesianGrid
                strokeDasharray="3 3"
                stroke="#2b2d42"
                opacity={0.6}
              />

              <XAxis
                dataKey="label"
                tick={{
                  fill: "#8b8da3",
                  fontSize: 12,
                }}
                axisLine={{
                  stroke: "#2b2d42",
                }}
                tickLine={false}
              />

              <YAxis
                tick={{
                  fill: "#8b8da3",
                  fontSize: 12,
                }}
                axisLine={false}
                tickLine={false}
              />

              <Tooltip
                contentStyle={{
                  background:
                    "#11121d",
                  border:
                    "1px solid #2b2d42",
                  borderRadius:
                    "12px",
                  color:
                    "#ffffff",
                }}
                cursor={{
                  fill:
                    "rgba(139,92,246,0.08)",
                }}
              />

              <Bar
                dataKey="value"
                fill="#8b5cf6"
                radius={[
                  8,
                  8,
                  0,
                  0,
                ]}
                maxBarSize={65}
              />

            </BarChart>

          </ResponsiveContainer>

        </div>

      </div>
    );
  }


  /* ==========================================================
     SCATTER
  ========================================================== */

  if (
    visualization.type ===
    "scatter"
  ) {

    return (
      <div className="data-visualization">

        <div className="visualization-header">

          <div>

            <div className="visualization-eyebrow">
              DATA VISUALIZATION
            </div>

            <h3>
              {visualization.title}
            </h3>

          </div>

          <span className="visualization-badge">
            SCATTER
          </span>

        </div>


        <div
          className="chart-container"
          style={{
            width: "100%",
            height: 340,
          }}
        >

          <ResponsiveContainer
            width="100%"
            height="100%"
          >

            <ScatterChart
              margin={{
                top: 15,
                right: 20,
                bottom: 20,
                left: 5,
              }}
            >

              <CartesianGrid
                strokeDasharray="3 3"
                stroke="#2b2d42"
                opacity={0.6}
              />

              <XAxis
                type="number"
                dataKey="x"
                name={
                  visualization.xLabel
                }
                tick={{
                  fill: "#8b8da3",
                  fontSize: 12,
                }}
                axisLine={{
                  stroke: "#2b2d42",
                }}
                tickLine={false}
              />

              <YAxis
                type="number"
                dataKey="y"
                name={
                  visualization.yLabel
                }
                tick={{
                  fill: "#8b8da3",
                  fontSize: 12,
                }}
                axisLine={false}
                tickLine={false}
              />

              <Tooltip
                cursor={{
                  strokeDasharray:
                    "4 4",
                }}
                contentStyle={{
                  background:
                    "#11121d",
                  border:
                    "1px solid #2b2d42",
                  borderRadius:
                    "12px",
                  color:
                    "#ffffff",
                }}
              />

              <Scatter
                data={
                  visualization.data
                }
                fill="#22d3ee"
              />

            </ScatterChart>

          </ResponsiveContainer>

        </div>

        <div className="scatter-labels">

          <span>
            X: {visualization.xLabel}
          </span>

          <span>
            Y: {visualization.yLabel}
          </span>

        </div>

      </div>
    );
  }


  return null;
}


/* ============================================================
   APP
============================================================ */

function App() {

  const [mode, setMode] =
    useState<Mode>("data");


  const [messages, setMessages] =
    useState<Message[]>([
      {
        id: 1,
        role: "assistant",
        mode: "data",
        content:
          "Hi! Upload a CSV and ask me a question about your data.",
      },
    ]);


  const [question, setQuestion] =
    useState("");


  const [selectedFile, setSelectedFile] =
    useState("");


  const [csvFilename, setCsvFilename] =
    useState("");


  const [isUploading, setIsUploading] =
    useState(false);


  const [csvUploading, setCsvUploading] =
    useState(false);


  const [isThinking, setIsThinking] =
    useState(false);


  /* ==========================================================
     PDF UPLOAD
  ========================================================== */

  const uploadDocument =
    async () => {

      const input =
        document.getElementById(
          "file-upload"
        ) as HTMLInputElement;

      const file =
        input?.files?.[0];

      if (!file) {
        alert(
          "Please select a PDF first."
        );
        return;
      }

      if (
        !file.name
          .toLowerCase()
          .endsWith(".pdf")
      ) {
        alert(
          "Only PDF files are supported."
        );
        return;
      }

      setIsUploading(true);

      const formData =
        new FormData();

      formData.append(
        "file",
        file
      );

      try {

        const response =
          await fetch(
            "http://127.0.0.1:8000/upload",
            {
              method: "POST",
              body: formData,
            }
          );

        const data =
          await response.json();

        if (
          !response.ok ||
          data.error
        ) {
          throw new Error(
            data.error ||
              "Upload failed."
          );
        }

        setSelectedFile(
          file.name
        );

        setMessages([
          {
            id: Date.now(),
            role: "assistant",
            mode: "document",
            content:
              `I've loaded "${file.name}". You can now ask questions about this document.`,
          },
        ]);

      } catch (error) {

        console.error(error);

        alert(
          "Something went wrong while uploading the PDF."
        );

      } finally {

        setIsUploading(false);

      }
    };


  /* ==========================================================
     CSV UPLOAD
  ========================================================== */

  const uploadCsv =
    async () => {

      const input =
        document.getElementById(
          "csv-upload"
        ) as HTMLInputElement;

      const file =
        input?.files?.[0];

      if (!file) {
        alert(
          "Please select a CSV first."
        );
        return;
      }

      if (
        !file.name
          .toLowerCase()
          .endsWith(".csv")
      ) {
        alert(
          "Only CSV files are supported."
        );
        return;
      }

      setCsvUploading(true);

      const formData =
        new FormData();

      formData.append(
        "file",
        file
      );

      try {

        const response =
          await fetch(
            "http://127.0.0.1:8000/data-upload",
            {
              method: "POST",
              body: formData,
            }
          );

        const data =
          await response.json();

        if (
          !response.ok ||
          data.error
        ) {
          throw new Error(
            data.error ||
              "CSV upload failed."
          );
        }

        setCsvFilename(
          file.name
        );

        setMessages([
          {
            id: Date.now(),
            role: "assistant",
            mode: "data",
            content:
              `I've loaded "${file.name}". Ask me anything about your dataset.`,
          },
        ]);

      } catch (error) {

        console.error(error);

        alert(
          "Something went wrong while uploading the CSV."
        );

      } finally {

        setCsvUploading(false);

      }
    };


  /* ==========================================================
     ASK QUESTION
  ========================================================== */

  const askQuestion =
    async () => {

      const trimmed =
        question.trim();

      if (
        !trimmed ||
        isThinking
      ) {
        return;
      }


      /* --------------------------------------------------------
         DOCUMENT VALIDATION
      -------------------------------------------------------- */

      if (
        mode === "document" &&
        !selectedFile
      ) {
        alert(
          "Please upload a PDF first."
        );
        return;
      }


      /* --------------------------------------------------------
         DATA VALIDATION
      -------------------------------------------------------- */

      if (
        mode === "data" &&
        !csvFilename
      ) {
        alert(
          "Please upload a CSV first."
        );
        return;
      }


      /* --------------------------------------------------------
         ADD USER MESSAGE
      -------------------------------------------------------- */

      const userMessage: Message =
        {
          id: Date.now(),
          role: "user",
          mode,
          content: trimmed,
        };


      setMessages(
        previous => [
          ...previous,
          userMessage,
        ]
      );


      setQuestion("");

      setIsThinking(true);


      try {


        /* ======================================================
           WEB SEARCH
        ====================================================== */

        if (
          mode === "web"
        ) {

          const response =
            await fetch(
              `http://127.0.0.1:8000/web-ask?query=${encodeURIComponent(
                trimmed
              )}`
            );


          const data =
            await response.json();


          if (!response.ok) {

            throw new Error(
              data.detail ||
                "Web search failed."
            );

          }


          setMessages(
            previous => [
              ...previous,

              {
                id:
                  Date.now() + 1,

                role:
                  "assistant",

                mode:
                  "web",

                content:
                  data.answer ||
                  "I couldn't find enough information on the web.",

                sources:
                  data.sources ||
                  [],
              },
            ]
          );


          return;
        }


        /* ======================================================
           DATA ANALYST
        ====================================================== */

        if (
          mode === "data"
        ) {

          const response =
            await fetch(
              `http://127.0.0.1:8000/data-ask?question=${encodeURIComponent(
                trimmed
              )}&filename=${encodeURIComponent(
                csvFilename
              )}`
            );


          const data =
            await response.json();


          if (!response.ok) {

            throw new Error(
              data.detail ||
                data.error ||
                "Dataset analysis failed."
            );

          }


          console.log(
            "DATA ANALYST RESPONSE:",
            data
          );


          setMessages(
            previous => [
              ...previous,

              {
                id:
                  Date.now() + 1,

                role:
                  "assistant",

                mode:
                  "data",

                content:
                  data.result ||
                  "I couldn't analyze the dataset.",

                visualization:
                  data.visualization ||
                  undefined,
              },
            ]
          );


          return;
        }


        /* ======================================================
           DOCUMENT RAG
        ====================================================== */

        if (
          mode === "document"
        ) {

          const conversation =
            messages
              .map(
                message =>
                  `${message.role}: ${message.content}`
              )
              .join("\n");


          const response =
            await fetch(
              `http://127.0.0.1:8000/ask?question=${encodeURIComponent(
                trimmed
              )}&conversation=${encodeURIComponent(
                conversation
              )}`
            );


          const data =
            await response.json();


          if (!response.ok) {

            throw new Error(
              data.detail ||
                "Document question failed."
            );

          }


          setMessages(
            previous => [
              ...previous,

              {
                id:
                  Date.now() + 1,

                role:
                  "assistant",

                mode:
                  "document",

                content:
                  data.answer ||
                  "I couldn't answer that question.",

                sources:
                  data.sources ||
                  [],
              },
            ]
          );


          return;
        }

      } catch (error) {

        console.error(error);


        const errorMessage =
          error instanceof Error
            ? error.message
            : "Something went wrong.";


        setMessages(
          previous => [
            ...previous,

            {
              id:
                Date.now() + 1,

              role:
                "assistant",

              mode,

              content:
                `Error: ${errorMessage}`,
            },
          ]
        );

      } finally {

        setIsThinking(false);

      }
    };


  /* ==========================================================
     ENTER KEY
  ========================================================== */

  const handleKeyDown =
    (
      event: KeyboardEvent<HTMLTextAreaElement>
    ) => {

      if (
        event.key === "Enter" &&
        !event.shiftKey
      ) {

        event.preventDefault();

        askQuestion();

      }

    };


  /* ==========================================================
     MODE CHANGE
  ========================================================== */

  const changeMode =
    (newMode: Mode) => {

      setMode(
        newMode
      );

      setQuestion("");

      if (
        newMode === "data"
      ) {

        setMessages([
          {
            id: Date.now(),
            role: "assistant",
            mode: "data",
            content:
              csvFilename
                ? `Your dataset "${csvFilename}" is ready. Ask me a question.`
                : "Upload a CSV and ask me anything about your dataset.",
          },
        ]);

      }


      if (
        newMode === "web"
      ) {

        setMessages([
          {
            id: Date.now(),
            role: "assistant",
            mode: "web",
            content:
              "Ask me anything and I'll search the web for current information.",
          },
        ]);

      }


      if (
        newMode === "document"
      ) {

        setMessages([
          {
            id: Date.now(),
            role: "assistant",
            mode: "document",
            content:
              selectedFile
                ? `Your document "${selectedFile}" is ready.`
                : "Upload a PDF and ask questions about it.",
          },
        ]);

      }

    };


  /* ==========================================================
     UI
  ========================================================== */

  return (

    <div className="app">


      {/* ======================================================
          SIDEBAR
      ====================================================== */}

      <aside className="sidebar">


        <div className="brand">

          <div className="brand-icon">
            AI
          </div>

          <div>

            <h1>
              Knowledge Copilot
            </h1>

            <p>
              Enterprise AI
            </p>

          </div>

        </div>


        {/* ====================================================
            MODE SWITCHER
        ==================================================== */}

        <div className="mode-switcher">

          <button
            className={
              mode === "document"
                ? "mode-button active"
                : "mode-button"
            }
            onClick={() =>
              changeMode(
                "document"
              )
            }
          >
            PDF
          </button>


          <button
            className={
              mode === "web"
                ? "mode-button active"
                : "mode-button"
            }
            onClick={() =>
              changeMode(
                "web"
              )
            }
          >
            Web
          </button>


          <button
            className={
              mode === "data"
                ? "mode-button active"
                : "mode-button"
            }
            onClick={() =>
              changeMode(
                "data"
              )
            }
          >
            Data
          </button>

        </div>


        {/* ====================================================
            DOCUMENT UPLOAD
        ==================================================== */}

        {mode === "document" && (

          <div className="sidebar-section">

            <p className="section-label">
              DOCUMENT
            </p>


            <label
              htmlFor="file-upload"
              className="upload-box"
            >

              <span className="upload-icon">
                ↑
              </span>

              <span>
                Choose PDF
              </span>

              <small>
                PDF files only
              </small>

            </label>


            <input
              id="file-upload"
              type="file"
              accept=".pdf,application/pdf"
              onChange={() => {}}
              hidden
            />


            <button
              className="upload-button"
              onClick={
                uploadDocument
              }
              disabled={
                isUploading
              }
            >

              {isUploading
                ? "Processing..."
                : "Upload document"}

            </button>

          </div>

        )}


        {/* ====================================================
            DATA UPLOAD
        ==================================================== */}

        {mode === "data" && (

          <div className="sidebar-section">

            <p className="section-label">
              DATASET
            </p>


            <label
              htmlFor="csv-upload"
              className="upload-box"
            >

              <span className="upload-icon">
                ↑
              </span>

              <span>
                Choose CSV
              </span>

              <small>
                CSV files only
              </small>

            </label>


            <input
              id="csv-upload"
              type="file"
              accept=".csv,text/csv"
              hidden
            />


            <button
              className="upload-button"
              onClick={
                uploadCsv
              }
              disabled={
                csvUploading
              }
            >

              {csvUploading
                ? "Processing..."
                : "Upload dataset"}

            </button>

          </div>

        )}


        {/* ====================================================
            ACTIVE DOCUMENT
        ==================================================== */}

        {mode === "document" &&
          selectedFile && (

            <div className="active-document">

              <div className="document-status">

                <span className="status-dot"></span>

                <span>
                  Active document
                </span>

              </div>


              <div className="document-name">
                {selectedFile}
              </div>

            </div>

          )}


        {/* ====================================================
            ACTIVE DATASET
        ==================================================== */}

        {mode === "data" &&
          csvFilename && (

            <div className="active-document">

              <div className="document-status">

                <span className="status-dot"></span>

                <span>
                  Active dataset
                </span>

              </div>


              <div className="document-name">
                {csvFilename}
              </div>

            </div>

          )}


        {/* ====================================================
            SIDEBAR BOTTOM
        ==================================================== */}

        <div className="sidebar-bottom">

          <div className="system-status">

            <span className="status-dot"></span>

            System online

          </div>


          <p>

            {mode === "data"
              ? "Ask natural-language questions about your CSV data."
              : mode === "web"
              ? "Answers are generated from current web sources."
              : "Answers are grounded in your uploaded documents."}

          </p>

        </div>

      </aside>


      {/* ======================================================
          MAIN
      ====================================================== */}

      <main className="chat-container">


        {/* ====================================================
            HEADER
        ==================================================== */}

        <header className="chat-header">

          <div>

            <p className="eyebrow">

              {mode === "data"
                ? "AI DATA WORKSPACE"
                : mode === "web"
                ? "WEB RESEARCH"
                : "DOCUMENT ASSISTANT"}

            </p>


            <h2>

              {mode === "data"
                ? "Analyze your data."
                : mode === "web"
                ? "Search the web."
                : "Ask your knowledge base."}

            </h2>


            <p className="header-description">

              {mode === "data"
                ? "Upload a CSV, ask natural-language questions, and visualize your data."
                : mode === "web"
                ? "Search current information from across the web."
                : "Ask questions and get answers grounded in your uploaded PDF."}

            </p>

          </div>


          <div className="header-status">

            <span className="status-dot"></span>

            Online

          </div>

        </header>


        {/* ====================================================
            MESSAGES
        ==================================================== */}

        <section className="messages">

          {messages.map(
            message => (

              <div
                key={
                  message.id
                }
                className={`message-row ${message.role}`}
              >


                {/* AI AVATAR */}

                {message.role ===
                  "assistant" && (

                  <div className="avatar assistant-avatar">

                    {message.mode ===
                    "data"
                      ? "▥"
                      : message.mode ===
                        "web"
                      ? "⌕"
                      : "AI"}

                  </div>

                )}


                <div className="message-content">


                  <div className="message-name">

                    {message.role ===
                    "assistant"
                      ? message.mode ===
                        "data"
                        ? "Data Analyst"
                        : message.mode ===
                          "web"
                        ? "Web Researcher"
                        : "Knowledge Copilot"
                      : "You"}

                  </div>


                  {/* MESSAGE */}

                  <div
                    className={`message-bubble ${message.role}`}
                  >

                    {message.content}

                  </div>


                  {/* ==================================================
                      VISUALIZATION
                  ================================================== */}

                  {message.role ===
                    "assistant" &&

                    message.mode ===
                      "data" &&

                    message.visualization && (

                      <DataVisualization
                        visualization={
                          message.visualization
                        }
                      />

                    )}


                  {/* ==================================================
                      SOURCES
                  ================================================== */}

                  {message.sources &&
                    message.sources.length >
                      0 && (

                    <div className="sources">

                      <div className="sources-title">
                        Sources
                      </div>


                      {message.sources.map(
                        (
                          source,
                          index
                        ) => (

                          <div
                            className="source-card"
                            key={`${source.source}-${source.page}-${index}`}
                          >

                            <div className="source-icon">
                              PDF
                            </div>


                            <div className="source-info">

                              <strong>
                                {
                                  source.source
                                }
                              </strong>

                              <span>
                                Page{" "}
                                {
                                  source.page
                                }
                              </span>

                            </div>

                          </div>

                        )
                      )}

                    </div>

                  )}

                </div>


                {/* USER AVATAR */}

                {message.role ===
                  "user" && (

                  <div className="avatar user-avatar">
                    You
                  </div>

                )}

              </div>

            )
          )}


          {/* ==================================================
              THINKING
          ================================================== */}

          {isThinking && (

            <div className="message-row assistant">

              <div className="avatar assistant-avatar">

                {mode === "data"
                  ? "▥"
                  : mode === "web"
                  ? "⌕"
                  : "AI"}

              </div>


              <div className="message-content">

                <div className="message-name">

                  {mode ===
                  "data"
                    ? "Data Analyst"
                    : mode ===
                      "web"
                    ? "Web Researcher"
                    : "Knowledge Copilot"}

                </div>


                <div className="message-bubble assistant thinking">

                  <span></span>

                  <span></span>

                  <span></span>

                </div>

              </div>

            </div>

          )}

        </section>


        {/* ====================================================
            INPUT
        ==================================================== */}

        <div className="input-area">

          <div className="input-wrapper">

            <textarea
              value={
                question
              }
              onChange={
                event =>
                  setQuestion(
                    event.target.value
                  )
              }
              onKeyDown={
                handleKeyDown
              }
              placeholder={
                mode === "data"
                  ? csvFilename
                    ? "Ask about your dataset..."
                    : "Upload a CSV to start..."
                  : mode === "web"
                  ? "Ask anything about the web..."
                  : selectedFile
                  ? "Ask a question about your document..."
                  : "Upload a PDF to start chatting..."
              }
              disabled={
                (mode ===
                  "document" &&
                  !selectedFile) ||

                (mode ===
                  "data" &&
                  !csvFilename) ||

                isThinking
              }
              rows={1}
            />


            <button
              className="send-button"
              onClick={
                askQuestion
              }
              disabled={
                !question.trim() ||
                isThinking ||
                (mode ===
                  "document" &&
                  !selectedFile) ||
                (mode ===
                  "data" &&
                  !csvFilename)
              }
              aria-label="Send message"
            >
              ↑
            </button>

          </div>


          <p className="input-hint">

            Press Enter to send · Shift + Enter
            for a new line

          </p>

        </div>

      </main>

    </div>
  );
}


export default App;