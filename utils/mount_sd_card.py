# https://www.youtube.com/watch?v=qL2g5YIVick&ab_channel=TechToTinker

def mount_sd_card(folder = "/sd"):
    import os
    from machine import Pin, SoftSPI
    from sdcard import SDCard

    """
    pin assignment
    vcc -> 5v
    gnd -> gnd
    cs -> g15
    sck -> g4
    mosi -> g17
    miso -> g18    

    """

    spisd = SoftSPI(
        -1,
        miso = Pin(18),
        mosi = Pin(17),
        sck = Pin(4)
    )
    sd = SDCard(spisd, Pin(15))

    vfs = os.VfsFat(sd)
    os.mount(vfs, folder)
    #os.chdir("sd")
    #print("sd card contains:", os.listdir())
    print(f"mounted sd card in '{folder}'")

if __name__ == "__main__":
    mount_sd_card()
    
    from os import listdir
    print(listdir("/sd"))

