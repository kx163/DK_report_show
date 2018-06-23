import dash_core_components as dcc
import dash_html_components as html


# #########
# The layout of the trial introduction board
# #########

content = dcc.Markdown('''
##### Overview

Intelligent Robots has finished a two-day trial at DK Fulfilment's Coventry warehouse on the 20th and 21st of March.
The trial was designed to be a functionality validation test for Intelligent Robots' robotic automation system, RPuck.

##### Installation

The test began with the installation of the system. The system to test consists of one robot, two stations, 
three trolleys and one WiFi access point.

According to discussion with DK fulfilment, the picking station was installed by the aisle and close to the middle 
of wine racks, while the packing station was installed close to DK's packing area. The distance between these 
two stations is at level of 30 meters.

This installation configuration is the configuration that Intelligent Robots tested most of the two days and is 
referenced as the **short run trial** through this report. However, Intelligent Robots has also tested another 
longer configuration at the after-work period, which is at level of 50 meters between stations. This longer 
configuration is referenced as the **long run trial** through this report.

By the other hand, as the *short run trial* was taken place during the work time and the *long run trial* was
taken place after work. We use the *short run trial*'s statistic model to simulate the busy period of the warehouse
and the *long run trial*'s statistic model to simulate the quiet period.

Intelligent Robots has also allocated one dedicated staff to monitor the safety of the test. This personnel has a 
certified remote emergency control and will trigger the control if there is an emergency case.

##### Result

Intelligent Robots has successfully validated the functionalities of their system. They have collected more than 30G
data from different sensors and concluded some statistical models of the system. The details of these statistic models
can be found in the **statistics** section of this report. Moreover, Intelligent Robots has also generated a predictive
model for their robotic automation system and this model can be found in the **prediction** section of this report.

Some quick and interesting conclusions:
* The execution time of a task can be decomposed into two main parts:
    * docking: which is the combination of two nearly fixed time operations:
        * catching the target trolley and leaving the start bay
        * entering the destination bay and dropping the trolley
    * navigation: which is the combination of two varying time operations, while the time is highly linear to the 
    station distance at a factor of robot's actual navigation speed:
        * navigate to the start bay, which is often negligible if the robot will continue a second task from the 
        previous destination bay
        * navigate to the destination bay, which is usually the most time consuming part of the task execution
* The total travelled distance, which could be treated as the total saved distance, is increasing slower and slower 
while the station distance increases. This leads to the existence of a most economic distance range, which is 50 meter 
to 100 meters for our DK prototype and is 100 meters to 200 meters for our next generation prototype.
'''
)

intro_div_id = "intro"
intro_layout = html.Div(
    id=intro_div_id,
    children=[
        html.H3(
            "DK Trial Introduction",
            style=dict(textAlign="center")
        ),
        content
    ]
)
