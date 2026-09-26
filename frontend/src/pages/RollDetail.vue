<script setup>
import { onMounted, ref, watch } from 'vue'
import { getJSON } from '../api'
import { widthCmLabel } from '../format'
import DropStripBar from '../components/DropStripBar.vue'

const props = defineProps({ id: String })
const roll = ref(null)

async function load() {
  roll.value = await getJSON(`/api/rolls/${props.id}`)
}
onMounted(load)
watch(() => props.id, load)
</script>
<template>
  <div class="page" v-if="roll"><h1>{{ roll.name }}</h1>
  <p v-if="roll.data_quality==='dirty'" class="warn">{{ roll.note }}</p>
  <p>幅宽 {{ widthCmLabel(roll) }} · 卷长 {{ roll.length }}m · 花距 {{ roll.pattern_cm }}cm</p>
  <section v-if="roll.example">
    <h2>示例测算</h2>
    <p>示例墙面周长 {{ roll.example.perimeter_m }}m、高 {{ roll.example.height_m }}m：
       <strong>{{ roll.example.drops }} 条</strong> · 每条 {{ roll.example.drop_len_m }}m ·
       每卷 {{ roll.example.strips_per_roll }} 条 · <strong>{{ roll.example.rolls }} 卷</strong></p>
    <DropStripBar :drops="roll.example.drops" :drop-len="roll.example.drop_len_m" :rolls="roll.example.rolls" />
  </section>
  <router-link to="/rolls">返回纸卷规格</router-link>
  </div>
</template>
