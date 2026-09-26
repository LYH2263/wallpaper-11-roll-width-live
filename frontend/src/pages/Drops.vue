<script setup>
import { onMounted, ref, watch } from 'vue'
import { getJSON } from '../api'
import DropStripBar from '../components/DropStripBar.vue'

const rolls = ref([])
const rollId = ref(null)
const detail = ref(null)

async function loadDetail() {
  if (rollId.value == null) return
  detail.value = await getJSON(`/api/rolls/${rollId.value}`)
}
onMounted(async () => {
  rolls.value = (await getJSON('/api/rolls')).items.filter(r => r.data_quality === 'clean')
  if (rolls.value.length) rollId.value = rolls.value[0].id
  await loadDetail()
})
watch(rollId, loadDetail)
</script>
<template>
  <div class="page"><h1>裁条预览</h1>
  <select v-model.number="rollId">
    <option v-for="r in rolls" :key="r.id" :value="r.id">{{ r.name }}（幅宽 {{ r.width_cm }} cm）</option>
  </select>
  <div v-if="detail?.example">
    <p>以「{{ detail.example.wall.name }}」展开：幅宽 {{ detail.width_cm }} cm，共 {{ detail.example.drops }} 幅。</p>
    <DropStripBar :drops="detail.example.drops" :drop-len="detail.example.drop_len_m" :rolls="detail.example.rolls" />
  </div>
  </div>
</template>
