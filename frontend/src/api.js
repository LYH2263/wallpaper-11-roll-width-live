async function requestJSON(method, path, body) {
  const opts = { method, headers: {} }
  if (body !== undefined) {
    opts.headers['Content-Type'] = 'application/json'
    opts.body = JSON.stringify(body)
  }
  const r = await fetch(path, opts)
  if (!r.ok) {
    let msg = `请求失败（${r.status}）`
    try {
      const j = await r.json()
      if (typeof j.detail === 'string') msg = j.detail
      else if (j.detail?.[0]?.msg) msg = j.detail[0].msg
      else msg = JSON.stringify(j)
    } catch { /* 保留默认原因 */ }
    throw new Error(msg)
  }
  return r.json()
}

export function getJSON(path) {
  return requestJSON('GET', path)
}
export function postJSON(path, body) {
  return requestJSON('POST', path, body)
}
export function patchJSON(path, body) {
  return requestJSON('PATCH', path, body)
}
