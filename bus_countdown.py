import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import io
from PIL import Image
from inky.auto import auto
import datetime 
inky = auto(ask_user=True, verbose=True)



###########################################################################
#####################User configurable data################################
###########################################################################
# Dictionary mapping stop IDs to given names
stops = {
    '490013766H': 'My bus stop 1',
    '490014585M': 'My bus stop 2',
    'another one': 'My bus stop 3',
    # Add more stop IDs and names as needed
}

#Define image configs
saturation = 0
buf = io.BytesIO()
vertical_spacing = 0.3  # Increase this value if text is overlapping
titlesize = 18
fontsize = 15
###########################################################################
###########################################################################
###########################################################################






# Function to truncate 'train-destination' if it's longer than 12 characters
def truncate_destination(destination):
    return (destination[:12] + '...') if len(destination) > 12 else destination

# List to store each item's data
data_list = []

for stop_id, given_name in stops.items():
    # Modify the URL for each stop
    url = f'https://tfl.gov.uk/bus/stop/{stop_id}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all 'li' elements
    lis = soup.find_all('li', class_='live-board-feed-item')

    # Extract data from each 'li'
    for li in lis:
        route_number = li.find('span', class_='live-board-route').text.strip()
        destination = truncate_destination(li.find('span', class_='train-destination').text.strip())  # Truncate if necessary
        eta = li.find('span', class_='live-board-eta').text.strip()

        # Create a dictionary for this item
        item_data = {
            'stop name': given_name,
            'live-board-route': route_number,
            'train-destination': destination,
            'live-board-eta': eta
        }

        # Add the dictionary to the list
        data_list.append(item_data)

# Adjusting the plot size to specific dimensions (800x480)
def plot_stop_data_specific_size(data_list):
    # Organize data by stop name
        stops_data = {}
        for item in data_list:
            stop_name = item['stop name']
            if stop_name not in stops_data:
                stops_data[stop_name] = []
            stops_data[stop_name].append(item)

        # Create a figure with specified dimensions
        fig = plt.figure(figsize=(800/100, 550/100))  # Adjust size as needed

        # Loop through each stop and create a subplot
        for i, (stop_name, items) in enumerate(stops_data.items(), start=1):
            ax = plt.subplot(len(stops_data), 1, i)
            ax.set_title(f"Stop: {stop_name}", fontsize=titlesize, color='white', backgroundcolor='red', loc='left')

            # Adjust the vertical spacing based on text size
            for j, item in enumerate(items[:3], start=1):
                plt.text(0.05, 1-j*vertical_spacing,
                        f"Route: {item['live-board-route']}, Destination: {item['train-destination']}, ETA: {item['live-board-eta']}",
                        fontsize=fontsize, color='white', backgroundcolor='red', verticalalignment='top', horizontalalignment='left')

            ax.axis('off')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)

        # Get current time and format it
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        # Display the current time on the top right corner of the plot
        plt.text(0.95, 0.95, current_time, horizontalalignment='right', verticalalignment='top', transform=plt.gcf().transFigure, fontsize=fontsize)

        plt.tight_layout()  # Optimize the layout
	# Adjust subplot margins
	#fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.2, hspace=0.3)
        fig.subplots_adjust(left=0.01, right=0.9, top=0.9, bottom=0.1, hspace=0.5)

# Call the function with specified size
plot_stop_data_specific_size(data_list)


plt.savefig(buf, format="png")
buf.seek(0)

plot_image = Image.open(buf).convert("RGB")
image = Image.new("RGB", (inky.width, inky.height), (255, 255, 255))
image.paste(plot_image, (0, 0))

inky.set_image(image, saturation=saturation)
inky.show()