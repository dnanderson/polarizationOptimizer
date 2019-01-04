import nidaqmx


def addChannel(task,device="cDAQ1Mod1",channel="ai0"):
    task.ai_channels.add_ai_voltage_chan(device + "/" + channel)
    return task

def updateTime(task,sampleRate,samples_per_chan):
    task.timing.cfg_samp_clk_timing(sampleRate, samps_per_chan = samples_per_chan)
    return task

def closeTask(task):
    task.close()
    return task

def initTask(device="cDAQ1Mod1",channel=["ai0"],sampleRate=10000,samples_per_chan=100):
    task = nidaqmx.Task()
    for k in range(len(channel)):
        task = addChannel(task,device=device,channel=channel[k])
    task = updateTime(task,sampleRate,samples_per_chan)
    return task

def get100data():
    with nidaqmx.Task() as task:
        # Configure task
        task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai0")
        task.timing.cfg_samp_clk_timing(10000, samps_per_chan = 100)
        # Read the data
        data = task.read(number_of_samples_per_channel=100)
        return data

def testDAQ():
    print("testDAQ")
    task = initTask()
    print(task.timing.samp_clk_rate)
    data = task.read(number_of_samples_per_channel=100)
    print(data)
    closeTask(task)


testDAQ()
