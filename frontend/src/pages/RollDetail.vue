<script setup>
import { onMounted, ref, watch } from 'vue'
import { getJSON } from '../api'
import DropStripBar from '../components/DropStripBar.vue'

const props = defineProps({ id: String })
const data = ref(null)
const err = ref('')

async function load() {
  err.value = ''
  try {
    data.value = await getJSON(`/api/rolls/${props.id}`)
  } catch (e) {
    err.value = e.message
  }
}
onMounted(load)
watch(() => props.id, load)
</script>
<template>
  <div class="page" v-if="data">
    <h1>{{ data.name }}</h1>
    <p>幅宽 <strong>{{ data.width_cm }}</strong> cm · 卷长 {{ data.length }} m · 花距 {{ data.pattern_cm }} cm</p>
    <p v-if="data.data_quality==='dirty'" class="warn">{{ data.note }}</p>

    <h2>示例测算</h2>
    <template v-if="data.example">
      <p>以「{{ data.example.wall.name }}」为例：
        <strong>{{ data.example.rolls }} 卷</strong> · {{ data.example.drops }} 条幅 ·
        每条 {{ data.example.drop_len_m }} m · 每卷 {{ data.example.strips_per_roll }} 条
      </p>
      <DropStripBar :drops="data.example.drops" :drop-len="data.example.drop_len_m" :rolls="data.example.rolls" />
    </template>
    <p v-else>暂无可用于示例的墙面。</p>

    <p><router-link to="/rolls">返回纸卷列表修改幅宽</router-link></p>
  </div>
  <div class="page" v-else-if="err"><p class="warn">{{ err }}</p></div>
</template>
