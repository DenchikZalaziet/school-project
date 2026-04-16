<template>
  <MusicBackground />
  <Header />
  <div class="scale_info container mt-3">
    <div class="scale-info-container text-center mt-4 mb-3" v-if="current_instrument && current_tuning && scale_name">
      <h3 class="scale-name fw-bold text-primary">
        <i class="bi bi-music-note-beamed me-2"></i>{{ scale_name }}
      </h3>
      <p class="scale-description text-muted fs-6 mt-2" v-if="scale_description">
        {{ scale_description }}
      </p>
    </div>

    <div class="selection-container mb-5 bg-white rounded-3 p-5 shadow-sm mx-auto" style="max-width: 1200px;">
      <div class="row g-5 align-items-start justify-content-center">
        <!-- Инструмент -->
        <div class="col-lg-5">
          <div class="form-group d-flex flex-column">
            <label class="form-label fw-bold mb-3 fs-5">
              <i class="bi bi-sliders me-2"></i>Инструмент
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
            <small class="text-muted mt-3 d-block fs-6 description-placeholder" :class="{ invisible: !instrumentDescription }">
              {{ instrumentDescription }}
            </small>
          </div>
        </div>

        <!-- Настройка -->
        <div class="col-lg-5">
          <div class="form-group d-flex flex-column">
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
            <small class="text-muted mt-3 d-block fs-6 description-placeholder" :class="{ invisible: !tuningDescription }">
              {{ tuningDescription }}
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

        <div class="playback-controls d-flex flex-column gap-3">
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

          <ScalePlayer 
            ref="player" 
            :intervals="scale_intervals" 
            :root-freq="rootFrequency" 
            class="ms-2" 
          />
        </div>
      </div>
    </div>
  </div>

  <div class="fretboard-wrapper">
    <div class="fretboard-container">
      <div v-if="scaleLoading" class="fretboard-loader-overlay">
        <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;"></div>
      </div>

      <div v-if="!current_instrument || !current_tuning" class="fretboard-placeholder">
        <p class="text-muted fs-5">Выберите инструмент и строй для отображения аппликатуры</p>
      </div>

      <transition v-else name="fade-slide" mode="out-in">
        <div class="fretboard" :key="fretboardKey">
          <div 
            v-for="(stringNotes, stringIndex) in scale_notes" 
            :key="`string-${stringIndex}`"
            class="string-row"
            :style="{ '--string-thickness': calculateThickness(stringIndex) + 'px'}"
          >
            <div class="open-note">
              <div class="fret-note" 
                @mouseenter="hoveredNote = instrument_notes[stringIndex][0]"
                @mouseleave="hoveredNote = null"
                @click="playNoteAudio(instrument_notes[stringIndex][0])"
                :class="{
                  'scale-note': stringNotes[0] !== '-',
                  'non-scale-note': stringNotes[0] === '-',
                  'root-note': isSameNote(instrument_notes[stringIndex][0], root),
                  'related-hover': hoveredNote && isSameNote(instrument_notes[stringIndex][0], hoveredNote),
                  'playing': playingNow === instrument_notes[stringIndex][0]
                }"
                :style="getNoteStyle(instrument_notes[stringIndex][0])"
              >
                <span class="note-label">{{ parseNote(instrument_notes[stringIndex][0]).name }}</span>
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
                @mouseenter="hoveredNote = instrument_notes[stringIndex][fretIndex + 1]"
                @mouseleave="hoveredNote = null"
                @click="playNoteAudio(instrument_notes[stringIndex][fretIndex + 1])"
                :class="{
                  'scale-note': scaleNote !== '-',
                  'non-scale-note': scaleNote === '-',
                  'root-note': isSameNote(instrument_notes[stringIndex][fretIndex + 1], root),
                  'related-hover': hoveredNote && isSameNote(instrument_notes[stringIndex][fretIndex + 1], hoveredNote),
                  'playing': playingNow === instrument_notes[stringIndex][fretIndex + 1]
                }"
                :style="getNoteStyle(instrument_notes[stringIndex][fretIndex + 1])"
              >
                <span class="note-label">{{ parseNote(instrument_notes[stringIndex][fretIndex + 1]).name }}</span>
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
              <span v-if="[3, 5, 7, 9, 12, 15, 17, 19, 21, 24].includes(n % 25)" class="fret-dot"></span>
              <span v-if="n % 12 === 0" class="fret-dot ms-2"></span>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import Header from '@/components/Header.vue';
import MusicBackground from '@/components/MusicBackground.vue';
import ScalePlayer from '@/components/ScalePlayer.vue';
import { useAuthStore } from '@/utils/auth_store';
import { api } from '@/utils/axios';

export default {
  name: 'InstrumentScaleView',
  components: {
    Header,
    MusicBackground,
    ScalePlayer
  },
  data() {
    return {
      loading: false,
      scaleLoading: false,
      current_instrument: null,
      current_tuning: null,
      scale_id: this.$route.params.scale_id,
      
      scale_name: "",
      scale_description: "",
      scale_intervals: [],

      all_instruments: [],
      all_tunings: [],

      prefer_flats: false,
      root: 'C',

      instrument_notes: [],
      scale_notes: [], 

      fretboardKey: 0,
      hoveredNote: null,
      playingNow: null,

      noteMap: {
        'C♯': 'D♭', 'D♯': 'E♭', 'F♯': 'G♭', 'G♯': 'A♭', 'A♯': 'B♭',
        'D♭': 'C♯', 'E♭': 'D♯', 'G♭': 'F♯', 'A♭': 'G♯', 'B♭': 'A♯'
      }
    };
  },
  computed: {
    availableNotes() {
      return this.prefer_flats 
        ? ["C", "D♭", "D", "E♭", "E", "F", "G♭", "G", "A♭", "A", "B♭", "B"]
        : ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"];
    },

    instrumentDescription() {
      return this.current_instrument ? `${this.current_instrument.category} • ${this.current_instrument.description}` : '';
    },

    tuningDescription() {
      return this.current_tuning?.description || '';
    },

    rootFrequency() {
      return this.getFrequency(this.root, 3);
    }
  },
  async created() {
    await this.fetchInitialData();
  },
  methods: {
    async fetchInitialData() {
      this.loading = true;
      await this.getScaleInfo();
      await this.getInstruments();
      this.loading = false;
    },

    async getScaleInfo() {
      const result = await api.get(`/scale/${this.scale_id}`, { 
        headers: { 'Authorization': `Bearer ${useAuthStore().token}` }
      });
      const scale = result.data;
      this.scale_name = scale.name;
      this.scale_description = scale.description;
      this.scale_intervals = scale.intervals || [];
    },

    async getInstruments() {
      const result = await api.get('/instrument');
      this.all_instruments = result.data;
      if (this.all_instruments.length > 0) {
        this.current_instrument = this.all_instruments[0];
        await this.getInstrumentTunings();
      }
    },

    async onInstrumentChange() {
      this.current_tuning = null;
      this.instrument_notes = [];
      this.scale_notes = [];
      if (this.current_instrument) {
        await this.getInstrumentTunings();
      }
    },

    async onTuningChange() {
      if (this.current_tuning) {
        await this.getInstrumentNotes();
      }
    },

    async getInstrumentTunings() {
      this.loading = true;
      api.get(`/instrument/${this.current_instrument._id}/tunings`)
      .then(async result => {
        this.all_tunings = result.data;
        if (this.all_tunings.length > 0) {
          this.current_tuning = this.all_tunings[0];
          await this.getInstrumentNotes();
        }
      }) 
      .finally(() => {
        this.loading = false;
      });
    },

    async getInstrumentNotes() {
      if (!this.current_tuning) return;
      this.scaleLoading = true;
      api.get(`/notes/${this.current_tuning._id}`, { 
        params: { prefer_flats: this.prefer_flats } 
      })
      .then(async result => {
        this.instrument_notes = result.data;
        await this.getScaleNotes();
      }) 
      .finally(() => {
        this.scaleLoading = false;
      });
    },

    async getScaleNotes() {
      if (!this.current_tuning || !this.scale_id) return;
      this.scaleLoading = true;
      await api.get(`/notes/${this.current_tuning._id}/${this.scale_id}`, {
        params: { prefer_flats: this.prefer_flats, root: this.root }
      })
      .then(result => {
        this.scale_notes = result.data;
        this.fretboardKey++; 
      }) 
      .finally(() => {
        this.scaleLoading = false;
      });
    },

    async setRootNote(note) {
      this.root = note;
      await this.getScaleNotes();
    },

    async togglePreference(useFlats) {
      if (this.prefer_flats === useFlats) return;
      this.prefer_flats = useFlats;
      if (this.noteMap[this.root]) {
        this.root = this.noteMap[this.root];
      }
      await this.getInstrumentNotes();
    },

    parseNote(noteStr) {
      if (!noteStr || noteStr === '-') return { name: '-', octave: null };
      const match = noteStr.match(/^([A-G][♯♭]?|[^0-9]+)(\d+)$/);
      return match ? { name: match[1], octave: parseInt(match[2]) } : { name: noteStr, octave: null };
    },

    isSameNote(n1, n2) {
      if (!n1 || !n2 || n1 === '-' || n2 === '-') return false;
      return this.parseNote(n1).name === this.parseNote(n2).name;
    },

    calculateThickness(index) {
      return Math.min(1 + 0.5 * index, 10);
    },

    getNoteStyle(noteStr) {
      const { name, octave } = this.parseNote(noteStr);
      if (name === '-') return {};
      const baseHue = 190;
      const hue = (baseHue + (octave * 20)) % 360;
      return {
        background: `linear-gradient(135deg, hsl(${hue}, 70%, 60%) 0%, hsl(${hue}, 80%, 40%) 100%)`,
        border: 'none'
      };
    },

    getFrequency(noteName, octave) {
      const flatsToSharps = { 'D♭': 'C♯', 'E♭': 'D♯', 'G♭': 'F♯', 'A♭': 'G♯', 'B♭': 'A♯' };
      const normalizedName = flatsToSharps[noteName] || noteName;
      const notes = ['C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B'];
      
      const noteIndex = notes.indexOf(normalizedName);
      if (noteIndex === -1) return 0;

      const a4Index = 9;
      const a4Octave = 4;
      const semitoneDistance = (octave - a4Octave) * 12 + (noteIndex - a4Index);

      return 440 * Math.pow(2, semitoneDistance / 12);
    },

    playNoteAudio(noteStr) {
      if (!noteStr || noteStr === '-') return;

      const parsed = this.parseNote(noteStr);
      if (parsed.octave === null) return;

      const freq = this.getFrequency(parsed.name, parsed.octave);
      if (!freq) return;

      if (this.$refs.player) {
        this.$refs.player.playSingleFrequency(freq);
      }

      this.playingNow = noteStr;
      setTimeout(() => {
        if (this.playingNow === noteStr) {
          this.playingNow = null;
        }
      }, 500);
    }
  }
};
</script>

<style scoped>
.fade-slide-enter-active, .fade-slide-leave-active {
  transition: all 0.3s ease;
}
.fade-slide-enter-from { opacity: 0; transform: translateY(10px); }
.fade-slide-leave-to { opacity: 0; transform: translateY(-10px); }

.selection-container {
  transition: opacity 0.3s ease;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
}
.selection-container.loading { opacity: 0.7; pointer-events: none; }

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
.custom-dropdown:disabled { background-color: #f8f9fa; color: #6c757d; cursor: not-allowed; }
.dropdown-wrapper { position: relative; }
.dropdown-loader { position: absolute; right: 15px; top: 50%; transform: translateY(-50%); z-index: 2; }
.form-group { display: flex; flex-direction: column; height: 100%; }

.scale-controls-container { margin-bottom: 2.5rem; }
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
.scale-controls.invisible { visibility: hidden; pointer-events: none; }
.root-note-selector, .preference-toggle { display: flex; align-items: center; gap: 1.5rem; }
.root-note-selector label, .preference-toggle label { font-weight: bold; color: #1a365d; min-width: 90px; margin-bottom: 0; }
.note-buttons { display: flex; flex-wrap: wrap; gap: 0.4rem; max-width: 500px; }
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
}
.note-button.active {
  background: #4da6ff;
  color: white;
  border-color: #1a365d;
}

.toggle-switch { display: flex; border: 2px solid #e0e0e0; border-radius: 10px; overflow: hidden; background: white; }
.toggle-option { padding: 0.8rem 1.5rem; border: none; background: transparent; cursor: pointer; font-weight: bold; }
.toggle-option.active { background: #4da6ff; color: white; }

.fretboard-wrapper { position: relative; min-height: 400px; }
.fretboard-container { position: relative; min-height: 450px; background: #f0f8ff; border-radius: 12px; padding: 25px; overflow-x: auto; }
.fretboard {
  display: inline-flex;
  flex-direction: column;
  background: linear-gradient(to bottom, #7edaff, #91caff);
  border-radius: 12px;
  padding: 20px 15px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
  min-width: 100%;
}
.fretboard-loader-overlay { position: absolute; inset: 0; background: rgba(240, 248, 255, 0.7); z-index: 10; display: flex; justify-content: center; align-items: center; }

.string-row { display: flex; align-items: center; position: relative; height: 55px; }
.string-row::after {
  content: '';
  position: absolute;
  left: 85px;
  right: 0;
  height: var(--string-thickness, 2px);
  background: linear-gradient(to right, #ddd, #fff, #ddd);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
  z-index: 1;
}
.open-note { width: 75px; display: flex; justify-content: center; align-items: center; z-index: 2; }
.open-note .fret-note { width: 45px; height: 45px; }

.nut { width: 10px; height: 110%; background: #333; z-index: 2; border-radius: 4px; }
.fret-cell { flex: 1; min-width: 65px; height: 100%; display: flex; justify-content: center; align-items: center; position: relative; border-right: 3px solid #333; }
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
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  z-index: 2;
  position: relative;
}
.fret-note:hover { transform: scale(1.15); filter: brightness(1.2); z-index: 5; }
.fret-note.related-hover { transform: scale(1.08); filter: brightness(1.1); box-shadow: 0 0 12px rgba(255, 255, 255, 0.5); }
.fret-note.playing { transform: scale(1.3); filter: brightness(1.5); box-shadow: 0 0 20px white; }

.root-note { border: 2px solid white !important; animation: pulse 2s infinite; }
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(255, 71, 87, 0.7); }
  70% { box-shadow: 0 0 0 10px rgba(255, 71, 87, 0); }
  100% { box-shadow: 0 0 0 0 rgba(255, 71, 87, 0); }
}
.non-scale-note { opacity: 0.5; filter: grayscale(0.5); }
.non-scale-note:hover, .non-scale-note.related-hover { opacity: 0.9; filter: grayscale(0); }
.root-indicator { position: absolute; top: -6px; right: -6px; background: #ff4757; color: white; border-radius: 50%; width: 20px; height: 20px; font-size: 11px; display: flex; align-items: center; justify-content: center; z-index: 3; }
.note-label { font-size: 15px; text-shadow: 1px 1px 2px rgba(0,0,0,0.5); }

.fret-markers { display: flex; margin-top: 15px; height: 25px; }
.fret-marker { flex: 1; min-width: 65px; display: flex; justify-content: center; align-items: center; position: relative; }
.fret-marker:first-child { width: 80px; min-width: 80px; flex: none; }
.fret-dot { width: 18px; height: 18px; border-radius: 50%; background-color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }

@media (max-width: 992px) {
  .fret-cell { min-width: 50px; }
  .fret-note { width: 36px; height: 36px; }
  .open-note { width: 65px; }
}
</style>
