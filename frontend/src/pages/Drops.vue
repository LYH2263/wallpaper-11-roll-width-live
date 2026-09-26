<script setup>
import { onMounted, ref, watch } from 'vue'
import { getJSON } from '../api'
import { widthCmLabel } from '../format'
import DropStripBar from '../components/DropStripBar.vue'

const rolls = ref([])
const rollId = ref(null)
const roll = ref(null)

onMounted(async () => {
  rolls.value = (await getJSON('/api/rolls')).items.filter(r => r.data_quality === 'clean')
  if (rolls.value.length) rollId.value = rolls.value[0].id
})
async function load() {
  if (rollId.value == null) return
  roll.value = await getJSON(`/api/rolls/${rollId.value}`)
}
watch(rollId, load)
</script>
<template>
  <div class="page"><h1>裁条预览</h1>
  <select v-model.number="rollId"><option v-for="r in rolls" :key="r.id" :value="r.id">{{ r.name }} · {{ widthCmLabel(r) }}</option></select>
  <div v-if="roll?.example">
    <p>按当前幅宽 {{ widthCmLabel(roll) }}，示例墙面展开 <strong>{{ roll.example.drops }}</strong> 幅：</p>
    <DropStripBar :drops="roll.example.drops" :drop-len="roll.example.drop_len_m" :rolls="roll.example.rolls" />
  </div>
  </div>
</template>
