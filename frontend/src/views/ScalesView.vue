<template>
  <MusicBackground />
  <Header />
  <Scales />
</template>

<script setup>
import Header from '@/components/Header.vue';
import MusicBackground from '@/components/MusicBackground.vue';
import Scales from '@/components/Scales.vue';
</script>

<script>
export default {
  name: 'Public Scales View'
}
</script>

<style scoped>
</style>
