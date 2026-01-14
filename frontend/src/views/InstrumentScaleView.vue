<template> 
  <Header></Header>

  <div class="container mt-4 p-1">
    <div class="selection-container mb-4 bg-white rounded-3 p-4 shadow-sm">
      <div class="row g-4 align-items-end">
        <div class="col-md-4">
          <div class="form-group h-100 d-flex flex-column">
            <label class="form-label fw-bold mb-3" style="color: var(--dark-blue);">
              <i class="bi bi-guitar me-2"></i>Инструмент
            </label>
            <div class="dropdown-wrapper position-relative flex-grow-1" :class="{ 'loading': loading }">
              <select 
                v-model="current_instrument" 
                @change="onInstrumentChange"
                class="form-select custom-dropdown"
                :disabled="loading"
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
            <small v-if="current_instrument" class="text-muted mt-2 d-block">
              {{ current_instrument.category }} • {{ current_instrument.description }}
            </small>
          </div>
        </div>
        
        <div class="col-md-4">
          <div class="form-group h-100 d-flex flex-column">
            <label class="form-label fw-bold mb-3" style="color: var(--dark-blue);">
              <i class="bi bi-music-note-list me-2"></i>Строй
            </label>
            <div class="dropdown-wrapper position-relative flex-grow-1" :class="{ 'loading': loading }">
              <select 
                v-model="current_tuning" 
                @change="onTuningChange"
                class="form-select custom-dropdown"
                :disabled="!current_instrument || loading"
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
            <small v-if="current_tuning" class="text-muted mt-2 d-block">
              {{ current_tuning.description }}
            </small>
          </div>
        </div>
      </div>
    </div>

    <div class="scale-controls" v-if="current_instrument && current_tuning">
      <div class="root-note-selector">
        <label class="mb-2">Тоника:</label>
        <div class="note-buttons">
          <button 
            v-for="note in availableNotes" 
            :key="note"
            class="note-button"
            :class="{ 
              'active': root === note,
              'flat-note': note.includes('♭'),
              'sharp-note': note.includes('♯')
            }"
            @click="root = note"
          >
            {{ note }}
          </button>
        </div>
      </div>

      <div class="preference-toggle">
        <label>Альтерация:</label>
        <div class="toggle-switch">
          <button 
            class="toggle-option"
            :class="{ 'active': !prefer_flats }"
            @click="prefer_flats = false"
          >
            ♯ Диез
          </button>
          <button 
            class="toggle-option"
            :class="{ 'active': prefer_flats }"
            @click="prefer_flats = true"
          >
            ♭ Бемоль
          </button>
        </div>
      </div>
      <button class="btn btn-primary apply-btn" 
        @click="getScaleNotes"
        :disabled="!showFretboard || scaleLoading"
        >
        <span v-if="scaleLoading" class="spinner-border spinner-border-sm me-2"></span>
        Применить
      </button>
    </div>
  </div>

  <div class="fretboard-container mt-4" v-if="showFretboard">
    <div v-if="scaleLoading" class="text-center py-5">
      <div class="spinner-border text-primary"></div>
      <p class="mt-2 text-muted">Загружаем аппликатуру...</p>
    </div>
    
    <div class="fretboard" v-else>
      <div 
        v-for="(stringNotes, stringIndex) in scale_notes" 
        :key="stringIndex"
        class="string-row"
        :style="{ '--string-thickness': calculateThickness(stringIndex) + 'px'}"
      >
        <div class="open-note">
          <div class="fret-note" 
            :class="{
              'scale-note': stringNotes[0] !== '-',
              'non-scale-note': stringNotes[0] === '-'
            }">
            <span class="note-label">{{ instrument_notes[stringIndex][0] }}</span>
            <span v-if="stringNotes[0] !== '-'" class="scale-indicator">•</span>
          </div>
        </div>
        
        <div class="nut"></div>
        
        <div 
          v-for="(note, fretIndex) in stringNotes.slice(1)" 
          :key="fretIndex"
          class="fret-cell"
        >
          <div v-if="note == '-'" class="fret-note non-scale-note">
            <span class="note-label">{{ instrument_notes[stringIndex][fretIndex + 1] }}</span>
          </div>
          <div v-else class="fret-note scale-note">
            <span class="note-label">{{ note }}</span>
            <span class="root-indicator" v-if="note === root">R</span>
          </div>
        </div>
      </div>
      
      <div class="fret-markers">
        <div class="fret-marker"></div>
        <div 
          v-for="n in instrument_notes[0].length - 1" 
          :key="n"
          class="fret-marker"
        >
          <span v-if="n % 12 === 0 || n % 12 === 3 || n % 12=== 5 || n % 12 === 7 || n % 12 === 9" 
                class="fret-dot"></span>
          <span v-if="n % 12 === 0" class="fret-dot ms-2"></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Header from '@/components/Header.vue';
import api from '@/utils/axios';
</script>

<script>
export default {
  name: 'Instrument Scale View',
  data() {
    return {
    	error_message: '',
      no_content: false,
      no_content_message: '',
      loading: false,
      scaleLoading: false,

			scale_id: this.$route.params.scale_id,
			current_instrument: null,
			current_tuning: null,

      all_instruments: [],
      all_tunings: [],

      prefer_flats: false,
      root: 'C',

      instrument_notes: [],
      scale_notes: [],
      string_count: 0,
      fretboard_length: 0,
    }
  },
  created() {
    this.getInstruments();
  },
  computed: {
    availableNotes() {
      if (this.prefer_flats) {
        return ["C", "D♭", "D", "E♭", "E", "F", "G♭", "G", "A♭", "A", "B♭", "B"];
      } else {
        return ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"];
      }
    },
    showFretboard() {
      return this.instrument_notes.length > 0 && this.scale_notes.length > 0;
    }
  },
  watch: {
    prefer_flats() {
      if (this.current_tuning) {
        this.getInstrumentNotes();
        if (this.scale_notes.length > 0) {
          this.getScaleNotes();
        }
      }
    }
  },
	methods: {
    calculateThickness(index) {
      return Math.min(1 + 0.5 * index, 10);
    },

    async getInstruments() {
      this.error_message = '';
      this.loading = true;
      api.get('/instrument') 
      .then(response => {
        this.all_instruments = [...response.data];
      })
      .catch(error => {
        console.error(error);
        this.error_message = error.response?.data?.detail ?? "Произошла ошибка";
      })
      .finally(() => {
        this.loading = false;
      });
    },

    async onInstrumentChange() {
      this.current_tuning = null;
      this.scale_notes = [];
      this.all_tunings = [];
      
      if (this.current_instrument) {
        this.string_count = this.current_instrument.number_of_strings;
        this.fretboard_length = this.current_instrument.fretboard_length;
        this.getInstrumentTunings();
      }
    },

    onTuningChange() {
      if (this.current_tuning) {
        this.getInstrumentNotes();
        this.getScaleNotes();
      }
    },

    async getInstrumentTunings() {
      this.error_message = '';
      this.loading = true;
      api.get(`/instrument/${this.current_instrument._id}/tunings`) 
      .then(response => {
        this.all_tunings = [...response.data];
      })
      .catch(error => {
        console.error(error);
        this.error_message = error.response?.data?.detail ?? "Произошла ошибка";
      })
      .finally(() => {
        this.loading = false;
      });
    },

    async getInstrumentNotes() {
      this.error_message = '';
      this.loading = true;
      api.get(`/notes/${this.current_tuning._id}`, {
        params: {
          prefer_flats: this.prefer_flats
        }
      })
      .then(response => {
        this.instrument_notes = [...response.data];
      })
      .catch(error => {
        console.error(error);
        this.error_message = error.response?.data?.detail ?? "Произошла ошибка";
      })
      .finally(() => {
        this.loading = false;
      });
    },

    getScaleNotes() {
      if (!this.current_tuning) return;
      
      this.error_message = '';
      this.scaleLoading = true;
      api.get(`/notes/${this.current_tuning._id}/${this.scale_id}`, {
        params: {
          prefer_flats: this.prefer_flats,
          root: this.root
        }
      })
      .then(response => {
        this.scale_notes = [...response.data];
      })
      .catch(error => {
        console.error(error);
        this.error_message = error.response?.data?.detail ?? "Произошла ошибка";
      })
      .finally(() => {
        this.scaleLoading = false;
      });
    }
	}
}
</script>

<style scoped>
.custom-dropdown {
  appearance: none;
  border: 2px solid var(--border-blue);
  border-radius: 8px;
  padding: 0.75rem 2.5rem 0.75rem 1rem;
  color: var(--dark-blue);
  font-weight: 500;
  transition: all 0.3s ease;
  width: 100%;
  height: 48px;
}

.custom-dropdown:focus {
  border-color: var(--primary-blue);
  box-shadow: 0 0 0 0.25rem rgba(77, 166, 255, 0.25);
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
  right: 12px;
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

.dropdown-wrapper {
  flex-grow: 1;
  min-height: 48px;
}

.scale-controls {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
  align-items: center;
  flex-wrap: wrap;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.root-note-selector, .preference-toggle {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.root-note-selector label, .preference-toggle label {
  font-weight: bold;
  color: var(--dark-blue);
  min-width: 80px;
  margin-bottom: 0;
}

.note-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
  max-width: 400px;
}

.note-button {
  padding: 0.5rem 0.8rem;
  border: 2px solid var(--border-blue);
  background: white;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: bold;
  min-width: 45px;
  font-size: 1rem;
}

.note-button:hover {
  background: var(--light-blue);
  transform: translateY(-2px);
}

.note-button.active {
  background: var(--primary-blue);
  color: white;
  border-color: var(--dark-blue);
  box-shadow: 0 2px 8px rgba(77, 166, 255, 0.3);
}

.flat-note {
  position: relative;
}

.sharp-note {
  position: relative;
}

.toggle-switch {
  display: flex;
  border: 2px solid var(--border-blue);
  border-radius: 8px;
  overflow: hidden;
  background: white;
}

.toggle-option {
  padding: 0.6rem 1.2rem;
  border: none;
  background: transparent;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: bold;
  min-width: 100px;
}

.toggle-option:hover {
  background: var(--light-blue);
}

.toggle-option.active {
  background: var(--primary-blue);
  color: white;
}

.apply-btn {
  padding: 0.6rem 1.5rem;
  font-weight: bold;
  min-width: 120px;
}

.fretboard-container {
  padding: 20px;
  overflow-x: auto;
  min-height: 300px;
}

.fretboard {
  display: inline-flex;
  flex-direction: column;
  position: relative;
  background: linear-gradient(to bottom, #7edaff, #91caff);
  border-radius: 8px;
  padding: 15px 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  min-width: 100%;
}

.string-row {
  display: flex;
  align-items: center;
  position: relative;
  height: 50px;
}

.string-row::after {
  content: '';
  position: absolute;
  left: 80px;
  right: 0;
  height: var(--string-thickness, 2px);
  background: linear-gradient(to right, #ddd, #fff, #ddd);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
  z-index: 1;
  border-radius: 2px;
  border-bottom: none;
  border-top: none;
}

.open-note {
  width: 70px;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2;
  color: #fff;
}

.open-note .fret-note {
  width: 40px;
  height: 40px;
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
  width: 8px;
  height: 110%;
  background: #333;
  z-index: 2;
  margin-right: 0;
  padding-right: 0;
  border-radius: 3px;
}

.fret-cell {
  flex: 1;
  min-width: 60px;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  border-right: 2px solid #333;
}

.fret-cell:last-child {
  border-right: none;
}

.fret-note {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  font-weight: bold;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
  transition: all 0.2s ease;
  cursor: pointer;
  z-index: 2;
  position: relative;
}

.scale-note {
  background-color: var(--dark-blue);
}

.scale-note:hover {
  background-color: var(--primary-blue);
  transform: scale(1.1);
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
  top: -5px;
  right: -5px;
  background: #ff4757;
  color: white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  font-size: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.note-label {
  font-size: 14px;
  font-weight: bold;
}

.fret-markers {
  display: flex;
  margin-top: 10px;
  height: 20px;
}

.fret-marker {
  flex: 1;
  min-width: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.fret-marker:first-child {
  width: 78px;
  min-width: 78px;
  flex: none;
}

.fret-dot {
  width: 15px;
  height: 15px;
  border-radius: 50%;
  background-color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 10px;
  color: #333;
  font-weight: bold;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .scale-controls {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .root-note-selector, .preference-toggle {
    width: 100%;
  }
  
  .note-buttons {
    max-width: 100%;
  }
  
  .fret-cell {
    min-width: 45px;
  }
  
  .fret-note {
    width: 32px;
    height: 32px;
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
    width: 68px;
    min-width: 68px;
  }
}

.selection-container {
  transition: opacity 0.3s ease;
}

.selection-container.loading {
  opacity: 0.7;
}
</style>
