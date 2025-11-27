<template> 
  <Header></Header>

  <div class="container mt-4 p-1">
    <div class="scale-controls">
      <div class="root-note-selector">
        <label class="">Тоника:</label>
        <div class="note-buttons">
          <button 
            v-for="note in availableNotes" 
            :key="note"
            class="note-button"
            :class="{ 
              'active': root === note,
              'flat-note': note.includes('b'),
              'sharp-note': note.includes('#')
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
      <button class="btn btn-primary" @click="getScaleNotes()">Применить</button>
    </div>
  </div>

  <div class="fretboard-container mt-1">
    <div class="fretboard">
      <div 
        v-for="(stringNotes, stringIndex) in scale_notes" 
        :key="stringIndex"
        class="string-row"
        :style="{ '--string-thickness': calculateThickness(stringIndex) + 'px'}"
      >
        <div class="open-note">
          <span class="note-label">{{ instrument_notes[stringIndex][0] }}</span>
        </div>
        
        <div class="nut"></div>
        
        <div 
          v-for="(note, fretIndex) in stringNotes.slice(1)" 
          :key="fretIndex"
          class="fret-cell"
        >
          <div v-if="note == '-'" class="fret-note fret-missing-note">
            <span class="note-label">{{ instrument_notes[stringIndex][fretIndex + 1] }}</span>
          </div>
          <div v-else class="fret-note">
            <span class="note-label">{{ note }}</span>
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

			scale_id: this.$route.params.scale_id,
			instrument_name: this.$route.params.instrument,
			tuning_name: this.$route.params.tuning,

      prefer_flats: false,
      root: 'C',

      instrument_notes: [[0]],
      scale_notes: [[0]],
      string_count: 0
    }
  },
  created() {
    this.getInstrumentNotes();
    this.getScaleNotes();
  },
  computed: {
    availableNotes() {
      return ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"];
    }
  },
	methods: {
    calculateThickness(index) {
      return Math.min(1 + 0.5 * index, 10);
    },
    async getInstrumentNotes() {
      this.error_message = '';
      this.loading = true;
      api.get(`/instrument/${this.instrument_name}/${this.tuning_name}`, {
        params: {
          prefer_flats: this.prefer_flats
        }
      })
      .then(response => {
        this.instrument_notes = [...response.data];
        this.string_count = this.instrument_notes.length;
      })
      .catch(error => {
        console.error(error);
        this.error_message = error.response?.data?.detail | "Произошла ошибка";
      })
      .finally(() => {
        this.loading = false;
      });
    },
    async getScaleNotes() {
      this.error_message = '';
      this.loading = true;
      api.get(`/instrument/${this.instrument_name}/${this.tuning_name}/${this.scale_id}`, {
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
        this.error_message = error.response?.data?.detail | "Произошла ошибка";
      })
      .finally(() => {
        this.loading = false;
      });
    }
	}
}
</script>

<style scoped>
.btn-outline-primary {
  color: var(--primary-blue);
  border-color: var(--primary-blue);
}

.btn-outline-primary:hover {
  background-color: var(--primary-blue);
  color: white;
}

.btn-primary {
  background-color: var(--primary-blue);
  border-color: var(--primary-blue);
  transition: all 0.3s;
}

.btn-primary:hover {
  background-color: var(--dark-blue);
  border-color: var(--dark-blue);
  transform: translateY(-2px);
}

.scale-controls {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
  align-items: center;
  flex-wrap: wrap;
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
}

.note-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
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
  font-style: italic;
  color: #666;
}

.sharp-note {
  font-weight: 800;
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
}

.toggle-option:hover {
  background: var(--light-blue);
}

.toggle-option.active {
  background: var(--primary-blue);
  color: white;
}

.fretboard-container {
  padding: 20px;
  overflow-x: auto;
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
  height: 40px;
}

.string-row::after {
  content: '';
  position: absolute;
  left: 60px;
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
  width: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2;
  color: #fff;
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
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: var(--dark-blue);
  color: white;
  font-weight: bold;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
  transition: all 0.2s ease;
  cursor: pointer;
  z-index: 2;
}

.fret-note:hover {
  background-color: var(--primary-blue);
  transform: scale(1.1);
}

.fret-missing-note {
  opacity: 0.7;
  background-color: #6693c0 !important;
  filter: grayscale(0.2);
}

.fret-missing-note:hover {
  opacity: 0.8;
  background-color: #7f8c8d !important;
  filter: grayscale(0.5);
  transform: scale(1.05);
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
  width: 58px; /* Open note + nut width */
  min-width: 58px;
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
  .fret-cell {
    min-width: 45px;
  }
  
  .fret-note {
    width: 30px;
    height: 30px;
  }
  
  .note-label {
    font-size: 12px;
  }
  
  .fret-marker {
    min-width: 45px;
  }
  
  .fret-marker:first-child {
    width: 53px;
    min-width: 53px;
  }
}
</style>