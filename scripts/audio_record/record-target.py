from machine import PDM_PCM
import uio
import time


def record_audio_blocking(filename, time_sec):
    rx_buf = bytearray([0] * 128)
    print("sample_rate:", pdm_pcm_config["sample_rate"])
    print("bits:", pdm_pcm_config["bits_per_sample"])
    print("format:", pdm_pcm_config["format"])
    print("decimation_rate:", 64)
    with uio.open(filename, "wb") as f:
        start_time = time.time()
        while time.time() - start_time < time_sec:
            print("[DEBUG] record_audio_blocking")
            num_read = pdm_pcm.readinto(rx_buf)
            print("[DEBUG] After readinto:", num_read)
            f.write(rx_buf[:num_read])
            print("[DEBUG] After write")


def record_audio_non_blocking(filename, time_sec):
    global data_ready
    data_ready = False

    def cback_data_ready(obj):
        global data_ready
        data_ready = True

    rx_buf = bytearray([0] * 1024)
    pdm_pcm.irq(cback_data_ready)

    with uio.open(filename, "wb") as f:
        start_time = time.time()
        while time.time() - start_time < time_sec:
            print("[DEBUG] record_audio_non_blocking")
            pdm_pcm.readinto(rx_buf)
            while not data_ready:
                pass

            data_ready = False
            f.write(rx_buf)


########################################
#### Audio configuration parameters ####
########################################

pdm_pcm_config = {
    "sample_rate": 16000,
    "bits_per_sample": 16,
    "format": PDM_PCM.STEREO,
    "mode": "blocking",
    "audio_file": "audio.raw",
    "time_sec": 5,
}

try:
    from scripts.audio_recording import audio_conf

    pdm_pcm_config = audio_conf.user_config
except ImportError:
    print("audio_conf.py not found. Using default config")

print("########## Audio configuration ##########")
print("format:          {}".format(pdm_pcm_config["format"]))
print("sample_rate:     {}".format(pdm_pcm_config["sample_rate"]))
print("bits_per_sample: {}".format(pdm_pcm_config["bits_per_sample"]))
print("mode:            {}".format(pdm_pcm_config["mode"]))
print("audio_file:      {}".format(pdm_pcm_config["audio_file"]))
print("time_sec:        {}".format(pdm_pcm_config["time_sec"]))
print("########################################")

if pdm_pcm_config["mode"] == "blocking":
    record_audio = record_audio_blocking
else:
    record_audio = record_audio_non_blocking

########################################

print("-- Starting audio recording...")
print("[DEBUG] Importing PDM_PCM...")
pdm_pcm = PDM_PCM(
    0,
    sck="P8_5",
    data="P8_6",
    sample_rate=pdm_pcm_config["sample_rate"],
    decimation_rate=64,
    bits=pdm_pcm_config["bits_per_sample"],
    format=pdm_pcm_config["format"],
    left_gain=0,
    right_gain=0,
)
print("constructed")
pdm_pcm.init()                    # ← 关键的一行
print("inited")
print("[DEBUG] Recording...")
record_audio(pdm_pcm_config["audio_file"], pdm_pcm_config["time_sec"])
pdm_pcm.deinit()

print("-- Audio recorded")