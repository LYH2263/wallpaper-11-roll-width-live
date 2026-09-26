// 幅宽展示唯一入口：直接使用服务端同源的 width_cm（由库内米值换算），前端不再自行乘 100
export function widthCmLabel(r) {
  const cm = Number(r?.width_cm)
  return Number.isFinite(cm) ? `${Number(cm.toFixed(2))}cm` : '—'
}
