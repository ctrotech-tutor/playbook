# Storage: the six-member behaviour contract

**Unreleased technical-review manuscript. Not added to production coverage counts or independently approved.**

Reviewed: 2026-10-17. Same-assistant normative reading and separately executed browser tests; not independent approval.

A Storage object is a synchronous string map, not a database transaction or a secret vault. These contracts cover all six direct declarations in the captured Storage interface. Window getter acquisition, event delivery and lifecycle/security boundaries are explained here as dependencies, not silently counted as independently completed owners.

## Objectives

- Predict every Storage member result and distinguish a missing entry from an empty string.

- Explain argument conversion and identify which step can throw before any mutation.

- Use storage without assuming insertion order, same-window events, unlimited capacity or permanent retention.

- Keep preferences optional and treat stored values as untrusted input.

## Prerequisites

- HTML Chapter 60: Where the wider APIs begin

- JavaScript functions, strict equality and try/catch

- The difference between an origin and a URL path

## Terms

- **DOMString:** A Web IDL string type; these members use JavaScript string conversion rather than JSON serialization.

- **opaque origin:** An origin that is not the normal scheme/host/port tuple, such as this book's isolated editor frame.

- **binding error:** Failure while checking the receiver, argument count or converting JavaScript arguments, before the HTML method steps.

- **broadcast:** Asynchronous storage-event scheduling for eligible other Storage objects.

- **quota:** A storage limit or policy boundary; an application should handle inability to save rather than assume a fixed available amount.

## Acquire the area inside the guarded operation

Storage is exposed on Window, not WorkerGlobalScope, and has no public constructor in this interface. Get an actual object through window.localStorage or window.sessionStorage. Their getters can throw SecurityError for an opaque origin or policy denial. This book's script-only sandbox has an opaque origin, so storage examples should be run on a dedicated local HTTP origin outside that editor. file: storage behaviour is not a portable tutorial environment. HTTPS is recommended for transport security; do not invent a SecureContext requirement on this IDL.

Sources: <https://html.spec.whatwg.org/multipage/webstorage.html#dom-localstorage-dev>, <https://html.spec.whatwg.org/multipage/webstorage.html#dom-sessionstorage-dev>, <https://html.spec.whatwg.org/multipage/webstorage.html#storage-2>, <https://html.spec.whatwg.org/multipage/webstorage.html#dns-spoofing-attacks>

## Storage scope is not a URL directory

localStorage is origin-associated state, subject to browser privacy policy and storage-key decisions. Paths such as /reader and /admin on one origin are not storage security boundaries. sessionStorage is also scoped to the top-level browsing context: same-origin frames in one tab can share it, while a separate tab has its own session area. An auxiliary context can start with a copy of the opener's session state; the copy is not ongoing shared session storage. A new tab is therefore not universally an empty-state guarantee.

Sources: <https://html.spec.whatwg.org/multipage/webstorage.html#dom-sessionstorage-dev>, <https://html.spec.whatwg.org/multipage/webstorage.html#dom-localstorage-dev>, <https://html.spec.whatwg.org/multipage/webstorage.html#cross-directory-attacks>, <https://storage.spec.whatwg.org/#storage-keys>

## Read the event in the receiving context

A storage broadcast excludes the mutating Storage object. For local storage, eligible other same-origin contexts can receive the event; session storage additionally requires the same top-level traversable. The queued event carries key, oldValue, newValue, the modifying document's URL and a storageArea object belonging to the receiver. It is not a synchronous callback from setItem and is not a cross-window lock. An inactive document can defer event processing. Equal-value setItem, missing-key removeItem and empty clear do not broadcast. Use a bounded observation in tests without treating elapsed silence as a proof that an event can never arrive.

Sources: <https://html.spec.whatwg.org/multipage/webstorage.html#concept-storage-broadcast>, <https://html.spec.whatwg.org/multipage/webstorage.html#the-storageevent-interface>

## Persistence, privacy and trust

localStorage is intended to outlive a page session, but browser settings, privacy controls and user clearing can remove data. A quota failure is not the only possible access failure, and feature presence alone does not prove a write will succeed. Do not put credentials or confidential documents in a teaching preference store. Same-origin script can read it, a key prefix is not access control, and values can have been written by another document or modified through developer tools. Validate values before use and never insert stored strings as trusted HTML.

Sources: <https://html.spec.whatwg.org/multipage/webstorage.html#privacy>, <https://html.spec.whatwg.org/multipage/webstorage.html#security-storage>, <https://html.spec.whatwg.org/multipage/webstorage.html#introduction-16>

## length

`readonly attribute unsigned long length;`

Count stored entries, not occupied bytes. An empty stored string still occupies one key/value pair.

### Inputs and conversions

This is a read-only attribute, not a method. Read it from a real Storage object. Its IDL type is unsigned long; the getter supplies a non-negative JavaScript integer.

### Return value and defaults

The current map size. It does not report remaining quota, character count or a constant capacity. There is no author-supplied default argument.

### Algorithm and branches

1. Read the associated storage map and return its size.

2. A write to an existing key changes its value without creating a second entry. A successful removal reduces the count.

### Errors and restrictions

Calling the extracted getter with a plain object fails the Web IDL receiver check with TypeError. Assigning to the read-only property is not a storage write: ordinary strict-mode JavaScript assignment throws TypeError; non-strict assignment can be ignored.

### Effects and ordering

Reading the count does not mutate the area or broadcast a storage event. Another document can change shared local state; a count followed by enumeration is not a locked snapshot.

```javascript
const area = sessionStorage;
const before = area.length;
area.setItem("ctro:empty", "");
console.log({ before, after: area.length, value: area.getItem("ctro:empty") });
area.removeItem("ctro:empty");
```

Run on a dedicated practice origin. If the example key was absent, length rises by one even though its stored value is empty.

Sources: <https://html.spec.whatwg.org/multipage/webstorage.html#dom-storage-length>, <https://webidl.spec.whatwg.org/#js-DOMString>, <https://webidl.spec.whatwg.org/#js-unsigned-long>, <https://webidl.spec.whatwg.org/#dfn-create-operation-function>

## key

`DOMString? key(unsigned long index);`

Look up a key name by position. The position is not a durable identifier.

### Inputs and conversions

One required unsigned long index, without Clamp or EnforceRange. Web IDL first converts through ToNumber, maps NaN and either infinity to zero, truncates finite fractions toward zero, and reduces modulo 2^32. Consequently key(-1) addresses 4294967295, while key(2 ** 32) addresses zero. null and an explicitly supplied undefined convert to zero. Symbol and BigInt cannot use this ToNumber conversion.

### Return value and defaults

The key at the converted index, or null when that index is at least the current entry count. A missing required argument is not a default-zero call: key() throws TypeError.

### Algorithm and branches

1. Convert and check the JavaScript call through the Web IDL binding.

2. Compare the converted index with the map size. Return null if it is outside the map.

3. Otherwise obtain the current map keys and return the key at that index.

### Errors and restrictions

Missing arguments, incompatible receivers, Symbol and BigInt numeric inputs can throw TypeError before the HTML steps. Object-to-number conversion may run author code and propagate its exception.

### Effects and ordering

Enumeration order is implementation-defined. Adding or removing keys can reorder entries. Replacing an existing value follows the no-reorder branch of setItem. If you need a sorted report, gather names and sort them explicitly; do not mutate the map inside index-based enumeration.

```javascript
const area = sessionStorage;
const names = [];
for (let i = 0; i < area.length; i += 1) {
  const name = area.key(i);
  if (name !== null) names.push(name);
}
names.sort();
console.log(names);
```

The result is an application-defined sorted list, not a claim about browser insertion order. Concurrent changes from another eligible document can still affect the snapshot; this loop does not add locking.

Sources: <https://html.spec.whatwg.org/multipage/webstorage.html#dom-storage-key>, <https://webidl.spec.whatwg.org/#js-DOMString>, <https://webidl.spec.whatwg.org/#js-unsigned-long>, <https://webidl.spec.whatwg.org/#dfn-create-operation-function>, <https://webidl.spec.whatwg.org/#abstract-opdef-converttoint>, <https://html.spec.whatwg.org/multipage/webstorage.html#concept-storage-reorder>

## getItem

`getter DOMString? getItem(DOMString key);`

Read the stored string for a key, preserving the distinction between absence and an empty value.

### Inputs and conversions

One required DOMString key. null becomes "null"; explicitly supplied undefined becomes "undefined". Those are actual key names. Objects undergo string conversion, which can run code or throw. A Symbol is not accepted by Web IDL ToString even though JavaScript String(symbol) has a special explicit-conversion behaviour.

### Return value and defaults

A string when present, including "", "false" or "0"; null when absent. No automatic JSON parsing, boolean conversion or fallback occurs. getItem() without the required argument throws TypeError.

### Algorithm and branches

1. Convert the key using the Web IDL binding.

2. If the map has no entry for that key, return null.

3. Otherwise return the stored value without parsing it.

### Errors and restrictions

A missing argument, Symbol input or incompatible receiver can throw TypeError. User-defined string conversion may throw a different exception. Accessing window.localStorage or window.sessionStorage is an earlier operation that can itself throw SecurityError; put the property access inside the guarded code.

### Effects and ordering

The read does not mutate storage or broadcast an event. Property-style reads are not interchangeable with getItem: an absent named property normally gives undefined, and API-name collisions can expose a prototype member instead of stored data.

```javascript
let value;
try {
  value = localStorage.getItem("ctro:theme");
} catch {
  value = null;
}
const theme = value === "night" ? "night" : "paper";
```

The allowlist treats storage as untrusted input. An absent, unavailable or unexpected preference falls back to paper. Use value === null when an application must distinguish absence from the stored empty string. Do not use value || fallback if empty is a meaningful saved value.

Sources: <https://html.spec.whatwg.org/multipage/webstorage.html#dom-storage-getitem>, <https://webidl.spec.whatwg.org/#js-DOMString>, <https://webidl.spec.whatwg.org/#js-unsigned-long>, <https://webidl.spec.whatwg.org/#dfn-create-operation-function>, <https://html.spec.whatwg.org/multipage/webstorage.html#dom-localstorage-dev>, <https://html.spec.whatwg.org/multipage/webstorage.html#dom-sessionstorage-dev>, <https://webidl.spec.whatwg.org/#legacy-platform-object-getownproperty>

## setItem

`setter undefined setItem(DOMString key, DOMString value);`

Create or replace one string-valued entry synchronously, subject to access and storage limits.

### Inputs and conversions

Two required DOMString arguments, converted in order: key and then value. setItem("x", null) stores "null"; setItem("x", undefined) stores "undefined". Omitting the value throws TypeError instead. Objects are not automatically serialized to JSON, and Symbol conversion throws.

### Return value and defaults

JavaScript undefined on success, not a promise, an entry count or a persistence certificate. There is no optional value or expiration default.

### Algorithm and branches

1. Start with oldValue = null and assume reordering may be needed.

2. If the key exists, read the old value. If it is the same string as the new value, return without mutation or broadcast. Otherwise mark that existing-value replacement must not reorder the map.

3. If the value cannot be stored, throw QuotaExceededError before changing this entry.

4. Set the map entry. Reorder only on the new-key branch. Broadcast the key, old string or null, and new string to eligible other Storage objects.

### Errors and restrictions

QuotaExceededError is a DOMException from the storage algorithm, not a promise rejection. Do not assume a universal free-space value or fill the real application origin to discover a quota. Binding/conversion errors can occur first. A failed replacement at the quota-check step retains the old value.

### Effects and ordering

A new key can reorder enumeration; an existing-key replacement does not. Equal-string writes produce no storage notification. Broadcast is asynchronous and does not notify the mutating Storage object itself. A synchronous return does not guarantee permanent disk retention or cross-window transaction locking.

```javascript
function saveTheme(theme) {
  if (theme !== "paper" && theme !== "night") {
    throw new TypeError("Unexpected theme");
  }
  try {
    localStorage.setItem("ctro:theme", theme);
    return true;
  } catch {
    return false;
  }
}
```

Validate the application value before writing. A false result means the preference was not saved, so keep the interface usable in memory and report that state without exposing private data. If you choose JSON, JSON.stringify and JSON.parse introduce their own errors and validation requirements.

Sources: <https://html.spec.whatwg.org/multipage/webstorage.html#dom-storage-setitem>, <https://webidl.spec.whatwg.org/#js-DOMString>, <https://webidl.spec.whatwg.org/#js-unsigned-long>, <https://webidl.spec.whatwg.org/#dfn-create-operation-function>, <https://html.spec.whatwg.org/multipage/webstorage.html#concept-storage-broadcast>, <https://html.spec.whatwg.org/multipage/webstorage.html#concept-storage-reorder>

## removeItem

`deleter undefined removeItem(DOMString key);`

Remove one key if it exists. Missing data is not an exceptional condition.

### Inputs and conversions

One required DOMString key, with the same null, undefined, Symbol and object-conversion rules as getItem. Calling removeItem() without a key fails binding validation.

### Return value and defaults

JavaScript undefined whether the key existed or not. It is not a boolean deletion result.

### Algorithm and branches

1. After argument conversion, return immediately if the map has no such key.

2. Otherwise remember its old string, remove the entry and reorder the map.

3. Broadcast the key, old string and newValue = null to eligible other Storage objects.

### Errors and restrictions

Missing arguments, incompatible receivers or invalid string conversion can fail before deletion. Acquisition of the storage object can already have failed with SecurityError. Removing a nonexistent key does not manufacture an error or a notification.

### Effects and ordering

A real removal can change enumeration order. The asynchronous event carries null as the new value. Application keys sharing one origin are not isolated by their names or URL directory.

```javascript
try {
  localStorage.removeItem("ctro:theme");
} catch {
  // Keep using the in-memory default.
}
```

Delete only the preference you own. Catching an access failure does not prove that a previously saved preference was removed. A privacy-sensitive feature must report a failed deletion rather than promising erasure.

Sources: <https://html.spec.whatwg.org/multipage/webstorage.html#dom-storage-removeitem>, <https://webidl.spec.whatwg.org/#js-DOMString>, <https://webidl.spec.whatwg.org/#js-unsigned-long>, <https://webidl.spec.whatwg.org/#dfn-create-operation-function>, <https://html.spec.whatwg.org/multipage/webstorage.html#concept-storage-broadcast>, <https://html.spec.whatwg.org/multipage/webstorage.html#cross-directory-attacks>

## clear

`undefined clear();`

Remove every entry in the selected storage area, including entries owned by other features on that origin.

### Inputs and conversions

No parameters. Extra JavaScript arguments are ignored by the Web IDL call; clear("ctro:") is not a prefix filter. Use the correct local or session area and an isolated practice origin.

### Return value and defaults

JavaScript undefined. An already-empty area is a successful no-op. This is not a certificate of physical erasure from backups, device storage or another area.

### Algorithm and branches

1. If the storage map is empty, return without broadcasting.

2. Otherwise clear the entire map.

3. Broadcast key = null, oldValue = null and newValue = null to eligible other Storage objects.

### Errors and restrictions

A wrong receiver can fail the binding check. Obtaining the selected storage area can throw SecurityError. clear has no key conversion: passing an object is not a request to inspect or stringify that object.

### Effects and ordering

A nonempty clear notifies eligible other documents asynchronously; an empty clear does not. It does not clear cookies, IndexedDB, the other Storage area or a server account. Do not use it as a general sign-out or application-reset implementation.

```javascript
// Dedicated, disposable practice origin only.
const area = sessionStorage;
area.setItem("ctro:one", "1");
area.setItem("another-feature", "keep?");
area.clear("ctro:");
console.log(area.length); // 0, not 1
```

The extra argument has no filtering meaning. For a namespaced reset, first collect matching key names, then remove each one. Collect before deleting because removal can reorder index-based enumeration.

Sources: <https://html.spec.whatwg.org/multipage/webstorage.html#dom-storage-clear>, <https://webidl.spec.whatwg.org/#js-DOMString>, <https://webidl.spec.whatwg.org/#js-unsigned-long>, <https://webidl.spec.whatwg.org/#dfn-create-operation-function>, <https://html.spec.whatwg.org/multipage/webstorage.html#concept-storage-broadcast>, <https://webidl.spec.whatwg.org/#dfn-overload-resolution-algorithm>

## Exercise

Implement a theme preference with exactly two accepted values: paper and night. The interface must work when storage is denied. Explain why getItem(key) || "paper", clear("ctro:"), a sorted assumption about key(0), and waiting for a same-document storage event are each unsuitable shortcuts.

### Explained answer

Read the Storage getter and getItem inside try/catch. Accept only paper or night and keep the chosen theme in memory when access or saving fails. Report that persistence is unavailable without breaking the theme control. A falsy fallback does not enforce the allowlist: an unexpected truthy string still passes through. Use an explicit null check when an empty string would be meaningful; a falsy fallback also conflates different saved values. clear ignores a prefix argument and removes all entries. key order is implementation-defined, so gather and sort names if ordering matters. Update this interface directly after a write, and use storage events only to react to eligible other documents. Catch a failed write or removal honestly: do not promise the value was saved or erased.

```html
<label for="theme-choice">Theme</label>
<select id="theme-choice">
  <option value="paper">Paper</option>
  <option value="night">Night</option>
</select>
<p id="theme-status" role="status"></p>
```

```javascript
function createThemePreference(applyTheme, reportPersistence) {
  const key = "ctro:theme";
  const accepted = new Set(["paper", "night"]);
  let theme = "paper";

  function read() {
    let stored;
    let readable = true;
    try {
      stored = window.localStorage.getItem(key);
    } catch {
      readable = false;
    }
    if (readable) theme = accepted.has(stored) ? stored : "paper";
    applyTheme(theme);
    reportPersistence(readable
      ? "Preference read; saving is not yet verified."
      : "Preference storage is unavailable.");
    return theme;
  }

  function set(next) {
    if (!accepted.has(next)) throw new TypeError("Unknown theme");
    theme = next;
    applyTheme(theme);
    let saved = true;
    try {
      window.localStorage.setItem(key, theme);
    } catch {
      saved = false;
    }
    reportPersistence(saved
      ? "Preference saved."
      : "Theme changed for this page only.");
    return saved;
  }

  return { read, set, get value() { return theme; } };
}
```

```javascript
const preference = createThemePreference(
  (theme) => {
    document.documentElement.dataset.theme = theme;
    document.getElementById("theme-choice").value = theme;
  },
  (message) => {
    document.getElementById("theme-status").textContent = message;
  }
);
preference.read();
document.getElementById("theme-choice").addEventListener("change", (event) => {
  preference.set(event.currentTarget.value);
});
```

The callbacks keep presentation outside the guarded storage call, so a rendering error is not misreported as a save failure. The in-memory value and control update immediately; another document does not need to send an event. A successful read does not promise a successful future write. Invalid stored text is ignored, not rendered as HTML. Put the scripts after this markup on a disposable HTTP origin. The fragment demonstrates preference state and honest status reporting; add matching theme styles in the application.

## Compatibility and continuing assessment

The browser report records 267 executed observations in exact Chromium, Firefox and WebKit versions, including both local and session Storage member probes. One WebKit observation needs triage: an unrelated automated page could read the changed local value but no event was observed there within 1,200 ms; an opener-connected peer did receive the expected events. This is not proof of permanent non-delivery or universal WebKit failure. Cross-agent-cluster interaction, automation context eligibility and current WPT evidence need review. Third-party storage policy, private browsing, all-device quotas and long-term retention remain separate assessment work.

## Still open

- Independent technical review of this unit and its answer.

- Unbounded/all-device privacy-policy and quota behaviour.

- Full inherited JavaScript/Web IDL platform-object semantics beyond the explicitly taught named-property boundaries.

- StorageEvent constructors and initStorageEvent as separate captured members.
