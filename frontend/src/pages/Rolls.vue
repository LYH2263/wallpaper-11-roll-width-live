<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, patchJSON } from '../api'
const items = ref([])
const drafts = ref({})
const errors = ref({})
const saving = ref({})

async function load() {
  items.value = (await getJSON('/api/rolls')).items
  for (const r of items.value) drafts.value[r.id] = String(r.width_cm ?? '')
}
onMounted(load)

async function saveWidth(r) {
  errors.value[r.id] = ''
  const v = Number(drafts.value[r.id])
  if (!Number.isFinite(v)) {
    errors.value[r.id] = '幅宽必须是数字（厘米）'
    return
  }
  saving.value[r.id] = true
  try {
    const updated = await patchJSON(`/api/rolls/${r.id}/width`, { width_cm: v })
    drafts.value[r.id] = String(updated.width_cm)
    await load()
  } catch (e) {
    errors.value[r.id] = e.message
  } finally {
    saving.value[r.id] = false
  }
}
</script>
<template>
  <div class="page"><h1>纸卷规格</h1>
  <div v-for="r in items" :key="r.id" class="roll-chip">
    <div>
      <router-link :to="`/rolls/${r.id}`"><strong>{{ r.name }}</strong></router-link>
      · 长{{ r.length }}m · 花距{{ r.pattern_cm }}cm
    </div>
    <label>幅宽
      <input v-model="drafts[r.id]" type="number" step="0.1" min="0" :disabled="saving[r.id]" /> cm
    </label>
    <button :disabled="saving[r.id]" @click="saveWidth(r)">保存幅宽</button>
    <span v-if="saving[r.id]">保存中…</span>
    <p v-if="errors[r.id]" class="warn">写入被拒：{{ errors[r.id] }}</p>
  </div>
  </div>
</template>
