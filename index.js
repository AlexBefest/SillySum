import { getContext, getApiUrl, doExtrasFetch } from "../../../extensions.js";

const extensionName = "chat-summarizer";
const extensionFolderPath = `scripts/extensions/third-party/${extensionName}`;
const extensionSettings = getContext().extension_settings[extensionName] || {};

async function summarizeChat() {
  const chatLog = getContext().chat;
  const chunkSize = 25;
  const chunks = [];

  for (let i = 0; i < chatLog.length; i += chunkSize) {
    chunks.push(chatLog.slice(i, i + chunkSize));
  }

  const summaries = [];

  for (const chunk of chunks) {
    chunk.push({ role: "user", content: "Summarize these messages in a fictional role-playing game and return a detailed recount of events in English." });

    const url = new URL(getApiUrl());
    url.pathname = '/api/summarize';

    const apiResult = await doExtrasFetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Bypass-Tunnel-Reminder': 'bypass',
      },
      body: JSON.stringify({
        extra_headers: {
          "HTTP-Referer": "your_site_url",
          "X-Title": "your_app_name",
        },
        model: "qwen/qwen-2.5-coder-32b-instruct",
        messages: chunk,
      }),
    });

    const summary = apiResult.choices[0].message.content;
    summaries.push(summary);
  }

  const combinedSummary = summaries.join(" ");
  console.log("Combined Summary:", combinedSummary);

  // Optionally, you can display the summary in the UI or save it to a file
  // For example, using toastr to show a popup:
  toastr.info(combinedSummary, "Chat Summary");
}

// Register a slash command to trigger the summarization
import { SlashCommandParser, SlashCommand, SlashCommandNamedArgument, ARGUMENT_TYPE } from "../../../script.js";

SlashCommandParser.addCommandObject(SlashCommand.fromProps({
  name: 'summarize',
  callback: summarizeChat,
  aliases: ['summarize-chat'],
  returns: 'a detailed summary of the chat in English',
  helpString: `
    <div>
      Summarizes the chat log in chunks and returns a detailed recount of events in English.
    </div>
    <div>
      <strong>Example:</strong>
      <ul>
        <li>
          <pre><code class="language-stscript">/summarize</code></pre>
        </li>
      </ul>
    </div>
  `,
}));