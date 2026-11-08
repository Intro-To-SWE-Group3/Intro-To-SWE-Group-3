/* ---------- API LAYER (swap this out later) ---------- */

const CURRENT_USER = "me";

const fakeDb = {
  conversations: [
    { id: 1, with: "Jordan P.", listing: "Calculus textbook", lastTime: "2:14 PM" },
    { id: 2, with: "Aisha K.", listing: "Mini fridge", lastTime: "Yesterday" },
    { id: 3, with: "Marcus T.", listing: "Desk lamp", lastTime: "Mon" },
  ],
  messages: {
    1: [
      { from: "Jordan P.", text: "Hey, is the textbook still available?", time: "2:10 PM" },
      { from: "me", text: "Yes it is! Want to meet at the library?", time: "2:12 PM" },
      { from: "Jordan P.", text: "Perfect, 4pm tomorrow works.", time: "2:14 PM" },
    ],
    2: [
      { from: "me", text: "Would you take $40 for the fridge?", time: "Yesterday" },
    ],
    3: [
      { from: "Marcus T.", text: "Does the lamp come with a bulb?", time: "Mon" },
    ],
  },
};

async function fetchConversations() {
  return fakeDb.conversations;
}

async function fetchMessages(conversationId) {
  return fakeDb.messages[conversationId] || [];
}

async function sendMessage(conversationId, text) {
  const msg = { from: CURRENT_USER, text, time: "Just now" };
  if (!fakeDb.messages[conversationId]) fakeDb.messages[conversationId] = [];
  fakeDb.messages[conversationId].push(msg);
  return msg;
}

/* ---------- UI ---------- */

const appEl = document.querySelector(".msg-app");
const convoList = document.getElementById("convoList");
const thread = document.getElementById("thread");
const chatTitle = document.getElementById("chatTitle");
const chatListing = document.getElementById("chatListing");
const composer = document.getElementById("composer");
const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const showInbox = document.getElementById("showInbox");

let activeId = null;
let conversations = [];

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function renderInbox() {
  convoList.replaceChildren();
  if (conversations.length === 0) {
    convoList.append(el("li", "empty", "No messages yet. Use Message seller on a listing to start one."));
    return;
  }
  for (const c of conversations) {
    const li = el("li");
    const btn = el("button", "convo" + (c.id === activeId ? " active" : ""));
    btn.type = "button";

    const top = el("div", "convo-top");
    top.append(el("span", "convo-name", c.with), el("span", "convo-time", c.lastTime));
    btn.append(top, el("div", "convo-item", c.listing));

    const msgs = fakeDb.messages[c.id] || [];
    if (msgs.length) btn.append(el("div", "convo-preview", msgs[msgs.length - 1].text));

    btn.addEventListener("click", () => openConversation(c.id));
    li.append(btn);
    convoList.append(li);
  }
}

function renderThread(messages) {
  thread.replaceChildren();
  if (messages.length === 0) {
    thread.append(el("p", "empty", "No messages yet. Say hello."));
    return;
  }
  for (const m of messages) {
    const bubble = el("div", "bubble " + (m.from === CURRENT_USER ? "mine" : "theirs"));
    bubble.append(document.createTextNode(m.text), el("small", "", m.time));
    thread.append(bubble);
  }
  thread.scrollTop = thread.scrollHeight;
}

async function openConversation(id) {
  activeId = id;
  const c = conversations.find((x) => x.id === id);
  chatTitle.textContent = c.with;
  chatListing.textContent = "About: " + c.listing;
  input.disabled = false;
  sendBtn.disabled = false;
  appEl.classList.add("in-chat");
  renderInbox();
  renderThread(await fetchMessages(id));
  input.focus();
}

composer.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text || activeId === null) return;
  input.value = "";
  await sendMessage(activeId, text);
  renderThread(await fetchMessages(activeId));
  renderInbox();
});

showInbox.addEventListener("click", () => appEl.classList.remove("in-chat"));

(async function init() {
  conversations = await fetchConversations();
  renderInbox();
})();
