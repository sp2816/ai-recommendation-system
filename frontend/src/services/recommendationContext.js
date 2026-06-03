const SEARCH_KEY = "anonymous_search_history";
const VIEW_KEY = "anonymous_view_history";
const MAX_ITEMS = 20;

function safeParse(value, fallback) {
  try {
    return JSON.parse(value) || fallback;
  } catch {
    return fallback;
  }
}

function readList(key) {
  if (typeof window === "undefined") {
    return [];
  }

  return safeParse(localStorage.getItem(key), []);
}

function writeList(key, value) {
  if (typeof window === "undefined") {
    return;
  }

  localStorage.setItem(
    key,
    JSON.stringify(value.slice(0, MAX_ITEMS))
  );
}

export function getLoggedInUser() {
  if (typeof window === "undefined") {
    return null;
  }

  return safeParse(localStorage.getItem("user"), null);
}

export function saveAnonymousSearch(searchQuery) {
  const query = (searchQuery || "").trim();

  if (!query) {
    return;
  }

  const history = readList(SEARCH_KEY);
  const next = [
    { query, created_at: new Date().toISOString() },
    ...history.filter((item) => item.query !== query)
  ];

  writeList(SEARCH_KEY, next);
}

export function saveAnonymousView(product) {
  if (!product?.article_id) {
    return;
  }

  const history = readList(VIEW_KEY);
  const entry = {
    article_id: String(product.article_id),
    product_name: product.product_name || product.prod_name || "",
    product_type_name: product.product_type_name || "",
    created_at: new Date().toISOString()
  };

  const next = [
    entry,
    ...history.filter((item) => item.article_id !== entry.article_id)
  ];

  writeList(VIEW_KEY, next);
}

export function getAnonymousActivity() {
  return {
    searches: readList(SEARCH_KEY),
    views: readList(VIEW_KEY)
  };
}

function tokenize(text) {
  return String(text || "")
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, " ")
    .split(/\s+/)
    .filter((token) => token.length >= 3);
}

export function rankAnonymousProducts(products) {
  const { searches, views } = getAnonymousActivity();

  if (!searches.length && !views.length) {
    return products;
  }

  const searchTokens = searches.flatMap((item) => tokenize(item.query));
  const viewedTypes = views
    .map((item) => item.product_type_name)
    .filter(Boolean)
    .map((type) => type.toLowerCase());

  const scored = products.map((product, index) => {
    const text = [
      product.product_name,
      product.product_type_name,
      product.product_group_name,
      product.description,
      product.colour_group_name
    ]
      .filter(Boolean)
      .join(" ")
      .toLowerCase();

    let score = 0;

    searchTokens.forEach((token) => {
      if (text.includes(token)) {
        score += 2;
      }
    });

    viewedTypes.forEach((type) => {
      if (String(product.product_type_name || "").toLowerCase() === type) {
        score += 3;
      }
    });

    return {
      product,
      score,
      index
    };
  });

  return scored
    .sort((left, right) => {
      if (right.score !== left.score) {
        return right.score - left.score;
      }

      return left.index - right.index;
    })
    .map((entry) => entry.product);
}
