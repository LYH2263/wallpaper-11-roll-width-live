async function send(path, options) {
  const r = await fetch(path, options)
  if (!r.ok) {
    const text = await r.text()
    let msg = text
    try {
      const body = JSON.parse(text)
      if (body && body.detail) msg = typeof body.detail === 'string' ? body.detail : JSON.stringify(body.detail)
    } catch {
      // 非 JSON 错误体，沿用原文
    }
    throw new Error(msg)
  }
  return r.json()
}

export function getJSON(path) {
  return send(path)
}
export function postJSON(path, body) {
  return send(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
}
export function patchJSON(path, body) {
  return send(path, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
}
