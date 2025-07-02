<template>
  <div class="calendar-heatmap">
    <v-calendar
      expanded
      :attributes="attributes"
      :model-value="new Date()"
      @dayclick="onDayClick"
    />
  </div>
  <ThreadListModal
    :open="isModalOpen"
    :date="selectedDate"
    :threads="selectedThreads"
    @close="isModalOpen = false"
  />
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useThreadStore } from '@/stores/thread'
import ThreadListModal from '@/components/profiles/ThreadListModal.vue'
import { format } from 'date-fns'
const threadStore = useThreadStore()


const selectedDate = ref(null)
const selectedThreads = ref([])
const isModalOpen = ref(false)

onMounted(() => {
  threadStore.fetchThreadHeatmap()  // 변경점: computed가 반응하므로 await 필요 없음
  isModalOpen.value = false
})

const attributes = computed(() => {
  const results = []

  for (const [dateStr, count] of Object.entries(threadStore.threadHeatmap ?? {})) {
    let fillMode = 'light'
    if (count === 1) fillMode = 'outline'
    else if (count >= 3) fillMode = 'solid'

    results.push({
      key: dateStr,
      dates: new Date(dateStr),
      highlight: {
        color: 'green',
        fillMode,
        contentClass: 'font-semibold text-black'
      },
      popover: { 
        label: `${count}개의 Thread`,
        visibility: 'hover',
        labelStyle: {
          backgroundColor: 'yellow',
          color: 'black'
        },
        // labelClass: 'custom-popover-label'
      }
    })
  }
  // 오늘 날짜 강조
  results.push({
    key: 'today',
    dates: new Date(),
    highlight: {
      color: 'blue',
      fillMode: 'outline',
      contentClass: 'border border-red-500'
    }
  })

  return results
})

const onDayClick = async ({ date }) => {
  const iso = format(date, 'yyyy-MM-dd')
  if (!threadStore.threadHeatmap?.[iso]) {
    alert('해당 날짜에 작성된 Thread가 없습니다.')
    isModalOpen.value = false
    return
  }
  selectedDate.value = iso
  try {
    const res = await threadStore.getThreadOnDate(iso)
    console.log(res)
    selectedThreads.value = res
    isModalOpen.value = true
  } catch (err) {
    console.error('Thread 조회 실패:', err)
  }
}
</script>

<style scoped>

.calendar-heatmap {
  max-width: 800px;
  margin: 0 auto;
  position: relative; /* ✅ ThreadListModal의 absolute 기준 */
}
</style>

<style>
::v-deep(.custom-popover-label) {
  background-color: white;
  color: black;
  padding: 6px 10px;
  border-radius: 6px;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}
</style>