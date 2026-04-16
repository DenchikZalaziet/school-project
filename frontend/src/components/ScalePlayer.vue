<template>
  <button 
      type="button" 
      class="btn btn-player rounded-pill px-4 d-inline-flex align-items-center gap-2 transition-all"
      :class="isPlaying ? 'btn-danger' : 'btn-outline-primary'"
      @click="toggleScalePlayback"
      :disabled="intervals.length === 0"
  >
      <span v-if="isPlaying" class="stop-icon"></span>
      <span v-else class="play-icon"></span>
      
      <span class="">{{ isPlaying ? 'Стоп' : 'Прослушать' }}</span>
      
      <span v-if="isPlaying" class="spinner-grow spinner-grow-sm" role="status"></span>
  </button>
</template>
  
<script>
export default {
  name: 'ScalePlayer',
  props: {
    intervals: {
      type: Array,
      required: true,
      default: () => []
    },
    rootFreq: { 
      type: Number, 
      default: 130.81 // C3
    }
  },
  data() {
    return {
      isPlaying: false,
      audioContext: null,
      activeNodes: [],
      shouldStop: false,
      playbackTimer: null
    }
  },
  beforeUnmount() {
    this.stopScale();
  },
  methods: {
    toggleScalePlayback() {
      this.isPlaying ? this.stopScale() : this.playScale(this.rootFreq);
    },
    
    stopScale() {
        this.shouldStop = true;
        this.isPlaying = false;
        
        if (this.playbackTimer) clearTimeout(this.playbackTimer);

        this.activeNodes.forEach(node => {
            try {
                node.stop();
                node.disconnect();
            } catch (e) {}
        });
        this.activeNodes = [];
    },

    async playSingleFrequency(freq) {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (!this.audioContext) this.audioContext = new AudioContext();
        if (this.audioContext.state === 'suspended') await this.audioContext.resume();

        const masterGain = this.audioContext.createGain();
        masterGain.gain.setValueAtTime(0.7, this.audioContext.currentTime); 
        masterGain.connect(this.audioContext.destination);

        this.playGuitarString(freq, this.audioContext.currentTime, 2.0, masterGain);
    },

    async playScale(rootFreq) {
        if (this.isPlaying) return;
        this.isPlaying = true;
        this.shouldStop = false;

        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (!this.audioContext) this.audioContext = new AudioContext();
        if (this.audioContext.state === 'suspended') await this.audioContext.resume();

        const masterGain = this.audioContext.createGain();
        masterGain.gain.setValueAtTime(0.7, this.audioContext.currentTime); 
        masterGain.connect(this.audioContext.destination);

        let timeOffset = 0.1;
        let notesToPlay = [0];
        let sum = 0;
        const baseFreq = rootFreq || 130.81; // C3
        
        this.intervals.forEach(i => {
            sum += i;
            notesToPlay.push(sum);
        });

        notesToPlay.forEach((semitones) => {
            const freq = baseFreq * Math.pow(2, semitones / 12);
            const startTime = this.audioContext.currentTime + timeOffset;
            this.playGuitarString(freq, startTime, 2.0, masterGain);
            timeOffset += 0.35;
        });

        this.playbackTimer = setTimeout(() => {
            if (!this.shouldStop) {
                this.isPlaying = false;
                this.activeNodes = [];
            }
        }, (timeOffset + 1.0) * 1000);
    },

    playGuitarString(freq, startTime, duration, targetNode) {
      const ctx = this.audioContext;
      const sampleRate = ctx.sampleRate;

      // ---- 1----
      const period = Math.floor(sampleRate / freq);
      const buffer = ctx.createBuffer(1, Math.ceil(sampleRate * duration), sampleRate);
      const data = buffer.getChannelData(0);

      let lastNoise = 0;
      for (let i = 0; i < period; i++) {
        const white = (Math.random() * 2 - 1) * 0.6;
        const filteredNoise = lastNoise * 0.8 + white * 0.2;
        data[i] = filteredNoise;
        lastNoise = filteredNoise;
      }

      // ---- 2. String resonance ----
      const sustainTime = 3.2;
      const feedback = Math.pow(0.005, 1 / (freq * sustainTime));
      let smoothing;
      if (freq < 100) smoothing = 0.6;       // very smooth for bass
      else if (freq < 300) smoothing = 0.4;  // warm mids
      else smoothing = 0.2;                  // still clear but not harsh highs

      for (let i = period; i < data.length; i++) {
        const a = data[i - period];
        const b = data[i - (period - 1)] || a;
        const avg = (a + b) / 2;
        data[i] = (data[i - period] * (1 - smoothing) + avg * smoothing) * feedback;
      }

      const source = ctx.createBufferSource();
      source.buffer = buffer;

      // ---- 3. Low‑pass ----
      const lowpass = ctx.createBiquadFilter();
      lowpass.type = "lowpass";
      // Cutoff frequency: lower for low notes, higher for high notes, but always below 3kHz
      lowpass.frequency.value = Math.min(2500, freq * 4);
      lowpass.Q.value = 0.7;   // smooth roll‑off

      // ---- 4. Warmth boost (low shelf, not aggressive) ----
      const warmth = ctx.createBiquadFilter();
      warmth.type = "lowshelf";
      warmth.frequency.value = 300;
      warmth.gain.value = 3; 

      // ---- 5. Stereo image----
      const splitter = ctx.createChannelSplitter(2);
      const merger = ctx.createChannelMerger(2);
      const delayL = ctx.createDelay();
      const delayR = ctx.createDelay();
      delayL.delayTime.value = 0;
      delayR.delayTime.value = 0.0025;

      // ---- 6. Envelope ----
      const envelope = ctx.createGain();
      envelope.gain.setValueAtTime(0, startTime);
      envelope.gain.linearRampToValueAtTime(1, startTime + 0.008);
      envelope.gain.exponentialRampToValueAtTime(0.005, startTime + duration);

      // ---- Routing ----
      source.connect(lowpass);
      lowpass.connect(warmth);
      warmth.connect(envelope);

      envelope.connect(delayL);
      envelope.connect(delayR);
      delayL.connect(merger, 0, 0);
      delayR.connect(merger, 0, 1);
      merger.connect(targetNode);

      source.start(startTime);
      source.stop(startTime + duration);
    }
  }
}
</script>

<style scoped>
.play-icon {
  width: 0; 
  height: 0; 
  border-top: 6px solid transparent;
  border-bottom: 6px solid transparent;
  border-left: 10px solid currentColor;
  display: inline-block;
}

.stop-icon {
  width: 10px;
  height: 10px;
  background-color: currentColor;
  display: inline-block;
}

.btn-player {
  transition: all 0.2s ease-in-out;
  border-width: 1px;
}

.btn-player:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.btn-player:active {
    transform: translateY(0);
}

.transition-all {
    transition: all 0.3s ease;
}
</style>
