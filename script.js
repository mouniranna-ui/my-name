const nouns = [
  "Atlas",
  "Lantern",
  "Pocket",
  "Pixel",
  "Sprout",
  "Nimbus",
  "Harbor",
  "Orbit",
  "Echo",
  "Bloom",
];

const types = [
  "portfolio",
  "recipe hub",
  "travel journal",
  "learning platform",
  "event page",
  "community board",
  "micro store",
  "newsletter landing",
  "habit tracker",
  "music discovery site",
];

const audiences = [
  "students",
  "remote workers",
  "new parents",
  "freelancers",
  "book lovers",
  "pet owners",
  "hikers",
  "small teams",
  "gamers",
  "creators",
];

const features = [
  "dark mode",
  "weekly digest emails",
  "AI-assisted suggestions",
  "community comments",
  "curated collections",
  "interactive map",
  "progress dashboard",
  "bookmarking",
  "public profiles",
  "mobile-first design",
];

function pick(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function uniquePicks(arr, count) {
  const copy = [...arr];
  const picks = [];

  while (copy.length && picks.length < count) {
    picks.push(copy.splice(Math.floor(Math.random() * copy.length), 1)[0]);
  }

  return picks;
}

function generateIdea() {
  const name = `${pick(nouns)} ${pick(nouns)}`;
  const type = pick(types);
  const audience = pick(audiences);
  const selectedFeatures = uniquePicks(features, 3);

  return {
    name,
    tagline: `A ${type} for ${audience}.`,
    meta: [
      `Primary audience: ${audience}`,
      `Core type: ${type}`,
      ...selectedFeatures.map((feature) => `Feature: ${feature}`),
    ],
  };
}

function renderIdeas(count) {
  const ideas = document.querySelector("#ideas");
  const template = document.querySelector("#idea-template");

  ideas.textContent = "";

  for (let i = 0; i < count; i += 1) {
    const idea = generateIdea();
    const node = template.content.cloneNode(true);

    node.querySelector(".name").textContent = idea.name;
    node.querySelector(".tagline").textContent = idea.tagline;

    const meta = node.querySelector(".meta");
    idea.meta.forEach((item) => {
      const li = document.createElement("li");
      li.textContent = item;
      meta.append(li);
    });

    ideas.append(node);
  }
}

const countInput = document.querySelector("#count");
const generateButton = document.querySelector("#generate");

generateButton.addEventListener("click", () => {
  const value = Number.parseInt(countInput.value, 10);
  const count = Number.isNaN(value) ? 3 : Math.max(1, Math.min(value, 12));
  countInput.value = String(count);
  renderIdeas(count);
});

renderIdeas(3);
