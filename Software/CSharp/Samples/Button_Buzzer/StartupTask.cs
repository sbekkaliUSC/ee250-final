// Turn the Buzzer on and Off with A Button
// In this example, we turn a buzzer on and off with a button.  


// The GrovePi connects the Raspberry Pi and Grove sensors.  
// You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi

// This example combines the GrovePi + Button + Buzzer
// http://www.dexterindustries.com/shop/grovepi-board/
// http://www.dexterindustries.com/shop/grove-buzzer/
// http://www.dexterindustries.com/shop/grove-button/

// Hardware Setup:
// Connect the Button to digital port 2
// Connect the Buzzer to digital port 5

/*
The MIT License(MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2016  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/

using System;
using Windows.ApplicationModel.Background;

// Add using statements to the GrovePi libraries
using GrovePi;
using GrovePi.Sensors;

namespace ButtonBuzzer
{
    public sealed class StartupTask : IBackgroundTask
    {
        public void Run(IBackgroundTaskInstance taskInstance)
        {
            // Connect the Button to digital port 2
            IButtonSensor button = DeviceFactory.Build.ButtonSensor(Pin.DigitalPin2);
            
            // Connect the Buzzer to digital port 5
            IBuzzer buzzer = DeviceFactory.Build.Buzzer(Pin.DigitalPin5);

            // Loop endlessly
            while (true)
            {
                try
                {
                    // Check the value of the button.
                    
                    string buttonon = button.CurrentState.ToString();
                    bool buttonison = buttonon.Equals("On", StringComparison.OrdinalIgnoreCase);

                    // Check the state of the buzzer.  This is just to output to debug!
                    SensorStatus status = buzzer.CurrentState;
                    bool buzzeron = status.ToString().Equals("On", StringComparison.OrdinalIgnoreCase);
        
                    // Print out Diagnostics.
                    System.Diagnostics.Debug.WriteLine("Button is " + buttonon);
                    System.Diagnostics.Debug.WriteLine("Buzzer is " + status.ToString());

                    // If the Button is on . . . .
                    if (buttonison)
                    {
                            buzzer.ChangeState(GrovePi.Sensors.SensorStatus.On);
                    } 
                    else
                    {
                            buzzer.ChangeState(GrovePi.Sensors.SensorStatus.Off);
                    }


                }
                catch (Exception ex)
                {
                    // NOTE: There are frequent exceptions of the following:
                    // WinRT information: Unexpected number of bytes was transferred. Expected: '. Actual: '.
                    // This appears to be caused by the rapid frequency of writes to the GPIO
                    // These are being swallowed here/

                    // If you want to see the exceptions uncomment the following:
                    // System.Diagnostics.Debug.WriteLine(ex.ToString());
                }
            }
        }
    }
}
