<template>
  <div class="music-bg" aria-hidden="true"></div>
</template>

<script>
export default {
  name: 'MusicBackground'
}
</script>

<style scoped>
.music-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: -1;
  background-repeat: repeat;
  background-size: 140px 140px, 170px 170px, 200px 200px, 240px 240px, 180px 180px;
  background-position: 0 0, 25px 35px, 60px 15px, 40px 70px, 80px 45px;
  background-image: 
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140' viewBox='0 0 140 140'%3E%3Ctext x='40' y='80' font-family='Arial, sans-serif' font-size='42' fill='rgba(0,0,0,0.03)' transform='rotate(-5, 40, 80)'%3E♪%3C/text%3E%3C/svg%3E"),
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='170' height='170' viewBox='0 0 170 170'%3E%3Ctext x='70' y='95' font-family='Arial, sans-serif' font-size='48' fill='rgba(0,0,0,0.03)' transform='rotate(8, 70, 95)'%3E♫%3C/text%3E%3C/svg%3E"),
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200' viewBox='0 0 200 200'%3E%3Ctext x='60' y='110' font-family='Arial, sans-serif' font-size='45' fill='rgba(0,0,0,0.03)' transform='rotate(12, 60, 110)'%3E♩%3C/text%3E%3C/svg%3E"),
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240' viewBox='0 0 240 240'%3E%3Ctext x='100' y='130' font-family='Arial, sans-serif' font-size='54' fill='rgba(0,0,0,0.03)' transform='rotate(-10, 100, 130)'%3E♬%3C/text%3E%3C/svg%3E"),
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180' viewBox='0 0 180 180'%3E%3Ctext x='50' y='100' font-family='Arial, sans-serif' font-size='40' fill='rgba(0,0,0,0.03)' transform='rotate(5, 50, 100)'%3E♭%3C/text%3E%3C/svg%3E");
}
</style>
