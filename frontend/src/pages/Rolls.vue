<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, patchJSON } from '../api'
import { widthCmLabel } from '../format'

const items = ref([])
const drafts = ref({})
const errors = ref({})
const saving = ref({})

onMounted(load)
async function load() {
  items.value = (await getJSON('/api/rolls')).items
}

function startEdit(r) {
  drafts.value[r.id] = r.width_cm
  errors.value[r.id] = ''
}
async function save(r) {
  const widthCm = Number(drafts.value[r.id])
  saving.value[r.id] = true
  errors.value[r.id] = ''
  try {
    const updated = await patchJSON(`/api/rolls/${r.id}/width`, { width_cm: widthCm })
    const i = items.value.findIndex(x => x.id === r.id)
    if (i >= 0) items.value[i] = { ...items.value[i], ...updated }
    drafts.value[r.id] = updated.width_cm
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
    <router-link :to="`/rolls/${r.id}`">{{ r.name }}</router-link>
    · 长{{ r.length }}m · 花距{{ r.pattern_cm }}cm
    · 幅宽
    <template v-if="drafts[r.id] !== undefined">
      <input v-model.number="drafts[r.id]" type="number" min="0" step="0.1" :disabled="saving[r.id]"> cm
      <button :disabled="saving[r.id]" @click="save(r)">保存幅宽</button>
    </template>
    <template v-else>
      <strong>{{ widthCmLabel(r) }}</strong>
      <button @click="startEdit(r)">改幅宽</button>
    </template>
    <p v-if="errors[r.id]" class="warn">写入被拒绝：{{ errors[r.id] }}</p>
  </div>
  </div>
</template>
