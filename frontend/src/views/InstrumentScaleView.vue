<template>
  <MusicBackground />
  <Header />
  <div class="container mt-3">
    <div class="selection-container mb-5 bg-white rounded-3 p-5 shadow-sm mx-auto" style="max-width: 1200px;">
      <div class="row g-5 align-items-end justify-content-center">
        <div class="col-lg-5">
          <div class="form-group h-100 d-flex flex-column">
            <label class="form-label fw-bold mb-3 fs-5">
              <i class="bi bi-guitar me-2"></i>Инструмент
            </label>
            <div class="dropdown-wrapper position-relative">
              <select 
                v-model="current_instrument" 
                @change="onInstrumentChange"
                class="form-select custom-dropdown py-3"
                :disabled="loading || all_instruments.length === 0"
              >
                <option value="" disabled>Выберите инструмент</option>
                <option 
                  v-for="instrument in all_instruments" 
                  :key="instrument._id"
                  :value="instrument"
                >
                  {{ instrument.name }}
                </option>
              </select>
              <div v-if="loading" class="dropdown-loader">
                <div class="spinner-border spinner-border-sm text-primary"></div>
              </div>
            </div>
            <small v-if="current_instrument" class="text-muted mt-3 d-block fs-6">
              {{ current_instrument.category }} • {{ current_instrument.description }}
            </small>
          </div>
        </div>
        
        <div class="col-lg-5">
          <div class="form-group h-100 d-flex flex-column">
            <label class="form-label fw-bold mb-3 fs-5">
              <i class="bi bi-music-note-list me-2"></i>Строй
            </label>
            <div class="dropdown-wrapper position-relative">
              <select 
                v-model="current_tuning" 
                @change="onTuningChange"
                class="form-select custom-dropdown py-3"
                :disabled="!current_instrument || loading || all_tunings.length === 0"
              >
                <option value="" disabled>Выберите строй</option>
                <option 
                  v-for="tuning in all_tunings" 
                  :key="tuning._id"
                  :value="tuning"
                >
                  {{ tuning.name }}
                </option>
              </select>
              <div v-if="loading" class="dropdown-loader">
                <div class="spinner-border spinner-border-sm text-primary"></div>
              </div>
            </div>
            <small v-if="current_tuning" class="text-muted mt-3 d-block fs-6">
              {{ current_tuning.description }}
            </small>
          </div>
        </div>
      </div>
    </div>

    <div class="scale-controls-container d-flex justify-content-center">
      <div class="scale-controls" :class="{ invisible: !(current_instrument && current_tuning) }">
        <div class="root-note-selector">
          <label class="mb-2 fs-5 fw-bold">Тоника:</label>
          <div class="note-buttons">
            <button 
              v-for="note in availableNotes" 
              :key="note"
              class="note-button"
              :class="{ 
                'active': isSameNote(root, note),
                'flat-note': note.includes('♭'),
                'sharp-note': note.includes('♯')
              }"
              @click="setRootNote(note)"
              type="button"
            >
              {{ note }}
            </button>
          </div>
        </div>

        <div class="preference-toggle">
          <label class="fs-5 fw-bold">Альтерация:</label>
          <div class="toggle-switch">
            <button 
              class="toggle-option"
              :class="{ 'active': !prefer_flats }"
              @click="togglePreference(false)"
              type="button"
            >
              ♯ Диез
            </button>
            <button 
              class="toggle-option"
              :class="{ 'active': prefer_flats }"
              @click="togglePreference(true)"
              type="button"
            >
              ♭ Бемоль
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="fretboard-wrapper" v-if="showFretboard">
    <div class="fretboard-container">
      <div v-if="scaleLoading" class="fretboard-loader">
        <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;"></div>
        <p class="mt-3 text-muted fs-5">Загружаем аппликатуру...</p>
      </div>
      
      <transition 
        name="fade-slide" 
        mode="out-in"
        @before-enter="beforeFretboardEnter"
        @enter="onFretboardEnter"
        @leave="onFretboardLeave"
      >
        <div class="fretboard" v-if="!scaleLoading && hasNotes" :key="fretboardKey">
          <div 
            v-for="(stringNotes, stringIndex) in scale_notes" 
            :key="`string-${stringIndex}-${current_instrument?._id}`"
            class="string-row"
            :style="{ '--string-thickness': calculateThickness(stringIndex) + 'px'}"
          >
            <div class="open-note">
              <div class="fret-note" 
                :class="{
                  'scale-note': stringNotes[0] !== '-',
                  'non-scale-note': stringNotes[0] === '-',
                  'root-note': isSameNote(instrument_notes[stringIndex][0], root)
                }">
                <span class="note-label">{{ instrument_notes[stringIndex][0] }}</span>
                <span v-if="stringNotes[0] !== '-'" class="scale-indicator">•</span>
                <span class="root-indicator" v-if="isSameNote(instrument_notes[stringIndex][0], root)">R</span>
              </div>
            </div>
            
            <div class="nut"></div>
            
            <div 
              v-for="(scaleNote, fretIndex) in stringNotes.slice(1)" 
              :key="`fret-${fretIndex}`"
              class="fret-cell"
            >
              <div 
                class="fret-note"
                :class="{
                  'scale-note': scaleNote !== '-',
                  'non-scale-note': scaleNote === '-',
                  'root-note': isSameNote(instrument_notes[stringIndex][fretIndex + 1], root)
                }"
              >
                <span class="note-label">{{ instrument_notes[stringIndex][fretIndex + 1] }}</span>
                <span class="root-indicator" v-if="isSameNote(instrument_notes[stringIndex][fretIndex + 1], root)">R</span>
              </div>
            </div>
          </div>
          
          <div class="fret-markers" v-if="instrument_notes.length > 0">
            <div class="fret-marker"></div>
            <div 
              v-for="n in instrument_notes[0].length - 1" 
              :key="n"
              class="fret-marker"
            >
              <span 
                v-if="n % 12 === 0 || n % 12 === 3 || n % 12 === 5 || n % 12 === 7 || n % 12 === 9" 
                class="fret-dot"
              ></span>
              <span v-if="n % 12 === 0" class="fret-dot ms-2"></span>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>

  <div v-if="!loading && !scaleLoading && (!hasNotes || !current_instrument || !current_tuning)" class="container text-center py-5">
    <h4 class="text-muted">Выберите инструмент и строй для отображения аппликатуры</h4>
  </div>
</template>

<script>
import MusicBackground from '@/components/MusicBackground.vue';
import Header from '@/components/Header.vue';
import { api } from '@/utils/axios';
import { env } from '@/utils/env.js';

export default {
  name: 'InstrumentScaleView',
  components: {
    Header,
    MusicBackground,
  },
  data() {
    return {
      error_message: '',
      loading: false,
      scaleLoading: false,
      current_instrument: null,
      current_tuning: null,
      scale_id: this.$route.params.scale_id,
      all_instruments: [],
      all_tunings: [],
      prefer_flats: false,
      root: 'C',
      instrument_notes: [],
      scale_notes: [],
      fretboardKey: 0,
      isAnimating: false,
      
      noteEquivalents: {
        'C♯': 'D♭',
        'D♯': 'E♭',
        'F♯': 'G♭',
        'G♯': 'A♭',
        'A♯': 'B♭',
        'D♭': 'C♯',
        'E♭': 'D♯',
        'G♭': 'F♯',
        'A♭': 'G♯',
        'B♭': 'A♯'
      },
      
      naturalNotes: ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
      
      cache: {
        instrumentNotes: new Map(),
        scaleNotes: new Map(),
        tunings: new Map()
      }
    };
  },
  computed: {
    availableNotes() {
      if (this.prefer_flats) {
        return ["C", "D♭", "D", "E♭", "E", "F", "G♭", "G", "A♭", "A", "B♭", "B"];
      } else {
        return ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"];
      }
    },
    hasNotes() {
      return this.instrument_notes.length > 0 && this.scale_notes.length > 0;
    },
    showFretboard() {
      return this.current_instrument && this.current_tuning;
    }
  },
  created() {
    this.getInstruments();
  },
  watch: {
    'current_instrument._id': {
      immediate: true,
      handler(newVal, oldVal) {
        if (newVal && newVal !== oldVal) {
          this.clearCacheForInstrument(newVal);
        }
      }
    }
  },
  methods: {
    calculateThickness(index) {
      return Math.min(1 + 0.5 * index, 10);
    },

    isSameNote(note1, note2) {
      if (!note1 || !note2) return false;
      if (note1 === note2) return true;
      
      if (this.noteEquivalents[note1] === note2) return true;
      if (this.noteEquivalents[note2] === note1) return true;
      
      if (this.naturalNotes.includes(note1) && this.naturalNotes.includes(note2)) {
        return note1 === note2;
      }
      
      return false;
    },

    setRootNote(note) {
      this.root = note;
      this.getScaleNotes();
    },

    convertNote(note, toFlats) {
      if (!note) return note;
      
      if (this.naturalNotes.includes(note)) return note;
      
      if (toFlats) {
        switch(note) {
          case 'C♯': return 'D♭';
          case 'D♯': return 'E♭';
          case 'F♯': return 'G♭';
          case 'G♯': return 'A♭';
          case 'A♯': return 'B♭';
          default: return note;
        }
      } else {
        switch(note) {
          case 'D♭': return 'C♯';
          case 'E♭': return 'D♯';
          case 'G♭': return 'F♯';
          case 'A♭': return 'G♯';
          case 'B♭': return 'A♯';
          default: return note;
        }
      }
    },

    togglePreference(useFlats) {
      if (this.prefer_flats === useFlats) return;
      
      const newRoot = this.convertNote(this.root, useFlats);
      
      this.prefer_flats = useFlats;
      this.root = newRoot;
      
      if (this.current_tuning) {
        const cacheKey = `${this.current_tuning._id}_${useFlats}`;
        this.cache.instrumentNotes.delete(cacheKey);
        
        this.instrument_notes = [];
        this.scale_notes = [];
        
        this.getInstrumentNotes();
      }
    },

    clearCacheForInstrument(instrumentId) {
      for (const key of this.cache.tunings.keys()) {
        if (key.startsWith(`${instrumentId}_`)) {
          this.cache.tunings.delete(key);
        }
      }
    },

    getCacheKey(tuningId, preferFlats, root) {
      return `${tuningId}_${preferFlats}_${root || ''}`;
    },

    getInstruments() {
      this.error_message = '';
      this.loading = true;
      
      api.get('/instrument')
        .then(response => {
          this.all_instruments = [...response.data];
          
          if (this.all_instruments.length > 0) {
            this.current_instrument = this.all_instruments[0];
            this.getInstrumentTunings();
          }
        })
        .catch(error => {
          if (env.DEBUG) {
            console.error(error);
          }
          this.error_message = error.response?.data?.detail ?? "Произошла ошибка";
        })
        .finally(() => {
          this.loading = false;
        });
    },

    onInstrumentChange() {
      this.current_tuning = null;
      this.instrument_notes = [];
      this.scale_notes = [];
      this.all_tunings = [];
      
      if (this.current_instrument) {
        this.getInstrumentTunings();
      }
    },

    onTuningChange() {
      if (this.current_tuning) {
        this.getInstrumentNotes();
      }
    },

    getInstrumentTunings() {
      if (!this.current_instrument) return;
      
      const cacheKey = `${this.current_instrument._id}_tunings`;
      
      if (this.cache.tunings.has(cacheKey)) {
        this.all_tunings = this.cache.tunings.get(cacheKey);
        if (this.all_tunings.length > 0) {
          this.current_tuning = this.all_tunings[0];
          this.getInstrumentNotes();
        }
        return;
      }
      
      this.error_message = '';
      this.loading = true;
      
      api.get(`/instrument/${this.current_instrument._id}/tunings`)
        .then(response => {
          this.all_tunings = [...response.data];
          
          this.cache.tunings.set(cacheKey, this.all_tunings);

          if (this.all_tunings.length > 0) {
            this.current_tuning = this.all_tunings[0];
            this.getInstrumentNotes();
          }
        })
        .catch(error => {
          if (env.DEBUG) {
            console.error(error);
          }
          this.error_message = error.response?.data?.detail ?? "Произошла ошибка";
        })
        .finally(() => {
          this.loading = false;
        });
    },

    getInstrumentNotes() {
      if (!this.current_tuning) return;
      
      const cacheKey = this.getCacheKey(this.current_tuning._id, this.prefer_flats, '');
      
      if (this.cache.instrumentNotes.has(cacheKey)) {
        this.instrument_notes = this.cache.instrumentNotes.get(cacheKey);
        this.getScaleNotes();
        return;
      }
      
      this.error_message = '';
      this.scaleLoading = true;
      this.fretboardKey++;
      
      api.get(`/notes/${this.current_tuning._id}`, {
        params: {
          prefer_flats: this.prefer_flats
        }
      })
        .then(response => {
          this.instrument_notes = [...response.data];
          
          this.cache.instrumentNotes.set(cacheKey, this.instrument_notes);
          
          this.getScaleNotes();
        })
        .catch(error => {
          if (env.DEBUG) {
            console.error(error);
          }
          this.error_message = error.response?.data?.detail ?? "Произошла ошибка";
          this.scaleLoading = false;
        });
    },

    getScaleNotes() {
      if (!this.current_tuning || !this.scale_id) return;
      
      const cacheKey = this.getCacheKey(this.current_tuning._id, this.prefer_flats, this.root);
      
      if (this.cache.scaleNotes.has(cacheKey)) {
        this.scale_notes = this.cache.scaleNotes.get(cacheKey);
        this.fretboardKey++;
        this.scaleLoading = false;
        return;
      }
      
      const wasAlreadyLoaded = this.scale_notes.length > 0;
      
      if (!wasAlreadyLoaded) {
        this.scaleLoading = true;
      }

      
      api.get(`/notes/${this.current_tuning._id}/${this.scale_id}`, {
        params: {
          prefer_flats: this.prefer_flats,
          root: this.root
        }
      })
        .then(response => {
          this.scale_notes = [...response.data];

          
          this.cache.scaleNotes.set(cacheKey, this.scale_notes);
          
          this.fretboardKey++;
        })
        .catch(error => {
          if (env.DEBUG) {
            console.error(error);
          }
          this.error_message = error.response?.data?.detail ?? "Произошла ошибка";
        })
        .finally(() => {
          this.scaleLoading = false;
        });
    },
    
    beforeFretboardEnter(el) {
      el.style.opacity = '0';
      el.style.transform = 'translateY(20px)';
    },
    
    onFretboardEnter(el, done) {
      this.isAnimating = true;
      
      requestAnimationFrame(() => {
        el.style.transition = 'all 0.3s ease';
        el.style.opacity = '1';
        el.style.transform = 'translateY(0)';
        
        setTimeout(() => {
          el.style.transition = '';
          this.isAnimating = false;
          done();
        }, 300);
      });
    },
    
    onFretboardLeave(el, done) {
      this.isAnimating = true;
      
      el.style.transition = 'all 0.3s ease';
      el.style.opacity = '0';
      el.style.transform = 'translateY(-20px)';
      
      setTimeout(() => {
        this.isAnimating = false;
        done();
      }, 300);
    }
  }
};
</script>

<style scoped>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(20px);
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.selection-container {
  transition: opacity 0.3s ease;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
}
.selection-container.loading {
  opacity: 0.7;
  pointer-events: none;
}

.custom-dropdown {
  appearance: none;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  padding: 1rem 3rem 1rem 1.5rem;
  color: #1a365d;
  font-weight: 500;
  transition: all 0.3s ease;
  width: 100%;
  height: 56px;
  font-size: 1.1rem;
}
.custom-dropdown:focus {
  border-color: #4da6ff;
  box-shadow: 0 0 0 0.35rem rgba(77, 166, 255, 0.25);
  outline: none;
}
.custom-dropdown:disabled {
  background-color: #f8f9fa;
  color: #6c757d;
  cursor: not-allowed;
}
.dropdown-wrapper {
  position: relative;
}
.dropdown-loader {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 2;
}
.form-group {
  display: flex;
  flex-direction: column;
  height: 100%;
}
.form-label {
  flex-shrink: 0;
}

.scale-controls-container {
  margin-bottom: 2.5rem;
}
.scale-controls {
  display: inline-flex;
  gap: 3rem;
  align-items: center;
  flex-wrap: wrap;
  padding: 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  max-width: 100%;
  border: 1px solid rgba(0,0,0,0.05);
}
.scale-controls.invisible {
  visibility: hidden;
  pointer-events: none;
}
.root-note-selector, .preference-toggle {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}
.root-note-selector label, .preference-toggle label {
  font-weight: bold;
  color: #1a365d;
  min-width: 90px;
  margin-bottom: 0;
}
.note-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  max-width: 500px;
}
.note-button {
  padding: 0.6rem 1rem;
  border: 2px solid #e0e0e0;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: bold;
  min-width: 52px;
  font-size: 1.1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.note-button:hover {
  background: #ebf8ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
.note-button.active {
  background: #4da6ff;
  color: white;
  border-color: #1a365d;
  box-shadow: 0 4px 12px rgba(77, 166, 255, 0.4);
  transform: translateY(-1px);
}
.toggle-switch {
  display: flex;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.toggle-option {
  padding: 0.8rem 1.5rem;
  border: none;
  background: transparent;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: bold;
  min-width: 110px;
  font-size: 1.1rem;
}
.toggle-option:hover {
  background: #ebf8ff;
  transform: translateY(-1px);
}
.toggle-option.active {
  background: #4da6ff;
  color: white;
  box-shadow: 0 2px 8px rgba(77, 166, 255, 0.3);
}

.fretboard-wrapper {
  position: relative;
  min-height: 400px;
  will-change: transform;
}
.fretboard-container {
  position: relative;
  height: 420px;
  padding: 25px;
  overflow-x: auto;
  background: #f0f8ff;
  border-radius: 12px;
}
.fretboard {
  display: inline-flex;
  flex-direction: column;
  background: linear-gradient(to bottom, #7edaff, #91caff);
  border-radius: 12px;
  padding: 20px 15px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
  min-width: 100%;
  border: 1px solid rgba(255,255,255,0.2);
  height: 100%;
}
.fretboard-loader {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: rgba(255,255,255,0.9);
  border-radius: 12px;
  z-index: 10;
}

.string-row {
  display: flex;
  align-items: center;
  position: relative;
  height: 55px;
}
.string-row::after {
  content: '';
  position: absolute;
  left: 85px;
  right: 0;
  height: var(--string-thickness, 2px);
  background: linear-gradient(to right, #ddd, #fff, #ddd);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
  z-index: 1;
  border-radius: 2px;
  border-bottom: none;
  border-top: none;
}
.open-note {
  width: 75px;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2;
  color: #fff;
}
.open-note .fret-note {
  width: 45px;
  height: 45px;
  position: relative;
}
.scale-indicator {
  position: absolute;
  bottom: 2px;
  right: 2px;
  font-size: 12px;
  color: #ffeb3b;
  font-weight: bold;
}
.nut {
  width: 10px;
  height: 110%;
  background: #333;
  z-index: 2;
  margin-right: 0;
  padding-right: 0;
  border-radius: 4px;
  box-shadow: inset 0 0 5px rgba(0,0,0,0.3);
}
.fret-cell {
  flex: 1;
  min-width: 65px;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  border-right: 3px solid #333;
}
.fret-cell:last-child {
  border-right: none;
}
.fret-note {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  font-weight: bold;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.3);
  transition: all 0.2s ease;
  cursor: pointer;
  z-index: 2;
  position: relative;
  font-size: 1rem;
}
.scale-note {
  background-color: #1a365d;
}
.scale-note:hover {
  background-color: #4da6ff;
  transform: scale(1.1);
}
.root-note {
  background-color: #ff4757 !important;
  animation: pulse 2s infinite;
}
.root-note:hover {
  background-color: #ff6b81 !important;
  transform: scale(1.1);
}
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(255, 71, 87, 0.7); }
  70% { box-shadow: 0 0 0 10px rgba(255, 71, 87, 0); }
  100% { box-shadow: 0 0 0 0 rgba(255, 71, 87, 0); }
}
.non-scale-note {
  opacity: 0.7;
  background-color: #6693c0 !important;
  filter: grayscale(0.2);
}
.non-scale-note:hover {
  opacity: 0.8;
  background-color: #7f8c8d !important;
  filter: grayscale(0.5);
  transform: scale(1.05);
}
.root-indicator {
  position: absolute;
  top: -6px;
  right: -6px;
  background: #ff4757;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  z-index: 3;
}
.note-label {
  font-size: 15px;
  font-weight: bold;
}
.fret-markers {
  display: flex;
  margin-top: 15px;
  height: 25px;
}
.fret-marker {
  flex: 1;
  min-width: 65px;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}
.fret-marker:first-child {
  width: 80px;
  min-width: 80px;
  flex: none;
}
.fret-dot {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background-color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 10px;
  color: #333;
  font-weight: bold;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

@media (max-width: 1200px) {
  .selection-container {
    max-width: 1000px !important;
  }
}
@media (max-width: 992px) {
  .selection-container {
    max-width: 800px !important;
  }
  .col-lg-5 {
    width: 100%;
    max-width: 500px;
    margin: 0 auto;
  }
  .scale-controls {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
    gap: 1.5rem;
    padding: 1.5rem;
  }
  .root-note-selector, .preference-toggle {
    width: 100%;
  }
  .note-buttons {
    max-width: 100%;
  }
  .fret-cell {
    min-width: 50px;
  }
  .fret-note {
    width: 36px;
    height: 36px;
  }
  .open-note {
    width: 65px;
  }
  .open-note .fret-note {
    width: 38px;
    height: 38px;
  }
  .note-label {
    font-size: 13px;
  }
  .fret-marker {
    min-width: 50px;
  }
  .fret-marker:first-child {
    width: 70px;
    min-width: 70px;
  }
  .custom-dropdown {
    height: 52px;
    font-size: 1rem;
  }
}
@media (max-width: 768px) {
  .selection-container {
    padding: 1.5rem !important;
  }
  .fret-cell {
    min-width: 45px;
  }
  .fret-note {
    width: 32px;
    height: 32px;
    font-size: 0.9rem;
  }
  .open-note {
    width: 60px;
  }
  .open-note .fret-note {
    width: 35px;
    height: 35px;
  }
  .note-label {
    font-size: 12px;
  }
  .fret-marker {
    min-width: 45px;
  }
  .fret-marker:first-child {
    width: 65px;
    min-width: 65px;
  }
  .scale-controls {
    padding: 1.2rem;
  }
  .note-button {
    min-width: 48px;
    padding: 0.5rem 0.8rem;
    font-size: 1rem;
  }
  .toggle-option {
    min-width: 100px;
    padding: 0.7rem 1.2rem;
    font-size: 1rem;
  }
}
</style>
