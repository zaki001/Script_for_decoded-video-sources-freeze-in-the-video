import os
import subprocess
import signal
from time import sleep

# Constants
VUE_CONFIG_FILE = "/opt/vue/config.d/30-avservice-loopback"

VUE_CONFIG_FILE = open ('30-avservice-loopback', 'w') 

def user_press_enter():
    input("Press enter to continue...\n")

def install_vue_loopback_config():
    if not os.path.isfile(VUE_CONFIG_FILE):
        print("Creating VUE config.d file 30-avservice-loopback")
        subprocess.run(["avs", "vue", "loopback"], check=True)

        print("Restarting VUE process - killall vue")
        subprocess.run(["killall", "vue"], check=True)

def run_mockinput(test_nb, video_size):
    process = subprocess.Popen(
        ["/opt/evertz/bin/mockinput", "-i100", video_size, "-s"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT
    )

    print(f"Step {test_nb} - Please confirm video plays test pattern and video resolution is {video_size}")
    user_press_enter()
    process.send_signal(signal.SIGTERM)  # This sends a termination signal to the process
    process.wait()  # Optional: wait for the process to properly terminate

def main():
    # Setup
    subprocess.run(["systemctl", "stop", "decoders"], check=True)
    install_vue_loopback_config()
    subprocess.run(["avs", "route", "preset", "1"], check=True)

    # Start Test
    print("Please clear the VUE layout, then add a Video Widget to the layout & assign to SDVN 1")
    user_press_enter()

    run_mockinput(1, "1920x1080")
    run_mockinput(2, "1280x720")
    run_mockinput(3, "960x540")
    run_mockinput(4, "2560x1440")
    run_mockinput(5, "640x480")
    run_mockinput(6, "3840x2160")
    run_mockinput(7, "1920x540")

    # Cleanup
    subprocess.run(["systemctl", "start", "decoders"], check=True)

    print("Done.")

if __name__ == "__main__":
    main()
