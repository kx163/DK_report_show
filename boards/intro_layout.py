import dash_core_components as dcc
import dash_html_components as html


# #########
# The layout of the trial introduction board
# #########

content = dcc.Markdown('''
##### Overview

Intelligent Robots completed a two-day trial at DK Fulfilment's Coventry warehouse on the 20th and 21st of March 2018. 
The trial was designed to be a functionality validation test for Intelligent Robots' robotic automation system, RPuck.

##### Installation

The test began with the installation of the system's hardware component infrastructure. This consisted one robot, 
two docking stations, three trolleys and one WiFi access point.

Following on from our discussions with DK fulfilment, the picking station was installed in a main travelling aisle and 
close to the midpoint of the racks storing wine, while the packing station was installed close to DK's main 
packing area. The distance between these two stations is 30 metres.

This installation configuration is what Intelligent Robots tested for most of the two days and is referred to as the 
**short run trial** throughout this report. However, Intelligent Robots also tested another, longer configuration at the 
after-work period, which had a distance 50 metres between stations. This longer configuration is referred to as the 
**long run trial**. We use the short run trial's statistic model to simulate the busy period of the warehouse and the 
long run trial's statistic model to simulate the quiet period.

Intelligent Robots also allocated one dedicated team member to monitor the system for safety purposes during the test. 
The individual had a certificated remote control that could trigger the system's emergency stop in any 
high risk situations.

##### Result

Intelligent Robots successfully validated all functionalities of the system. We collected more than 30GB of data 
from different sensors and created statistical models from this data to evaluate system performance. The details of 
these models can be found in the **statistics** section of this report. Moreover, Intelligent Robots has generated 
a predictive model for their robotic automation system, which can be found in the **prediction** section of this report.

Some headline conclusions:
* The execution time of a task can be decomposed into two main parts:
    * docking: the combination of two nearly fixed time operations:
        * catching the target trolley and leaving the start bay
        * entering the destination bay and dropping the trolley
    * navigation: the combination of two varying time operations, while the time is highly linear to the 
    station distance at a factor of robot's actual navigation speed:
        * navigate to the start bay, which is often negligible if the robot will continue a second task from 
        the previous destination bay
        * navigate to the destination bay, which is usually the most time consuming part of the task execution
* The rate of change of total travelled distance (which we use as a proxy for the total walking saved distance) 
increases at a slower rate as the station distance increases. This leads to the existence of an economically 
optimal distance range, which is 50 to 100 metres for our DK prototype and 100 to 200 metres for 
our next generation prototype.
'''
)

intro_div_id = "overview"
intro_layout = html.Div(
    id=intro_div_id,
    children=[
        html.H3(
            "DK Trial Overview",
            style=dict(textAlign="center")
        ),
        content
    ]
)
