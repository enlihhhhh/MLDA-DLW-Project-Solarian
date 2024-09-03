# Solarian 
<hr style="border:2px solid gray"> 

<img width="1438" alt="Screenshot 2022-10-03 at 3 29 42 AM" src="https://user-images.githubusercontent.com/101797615/193472656-d9f53296-f72b-4e76-8939-36f773f55fac.png">

## ℹ Background and Introduction
> *"Develop AI models or IoT solutions that solve industrial or social problems in the new stage of society development. The Smart Nation is an initiative by the Government of Singapore to harness from info-comm technologies, networks and big data to create tech-enabled solutions."* 

Through this hackathon, our group aims to develop AI models to help solve problems faced by the current society.

Among the seven National AI Projects that address Key Challenges in Singapore, we decided to focus on the Smart Estate section. Our objective is to provide people and companies the necessary information about solar panels to better help them install them at the respective places.

Studies have shown that Singapore has a high average annual solar irradiation of about 1,580 kWh/m2 makes solar photovoltaic (PV) a potential renewable energy option for Singapore. With increase in global temperature around the world and lack of natural resources, Singapore is looking to divert more attention to renewable energy. However, we have limited available land for the large scale deployment of solar panels, hence it is more viable to deploy solar panels at rooftop of houses in Singapore. As such, technologies that boost the use of solar power will ultimately help SG transition to a fully sustainable Smart Nation

## ❓ Problem Statement
> How can we detect and classify Commercial and Industrial rooftops in Singapore with the help of AI in order to identify the potential of solar panel installations?

## 💡 Solution
> A computer-vision based system that helps users to determine where to best deploy different type of solar panels
Our solution works by **calculating performance ratios** of Monocrystal Solar Panels, adjusted for average irradiance over different regions in Singapore. The computer-vision based model is trained using a dataset found from kaggle: [here](https://www.kaggle.com/datasets/humansintheloop/semantic-segmentation-of-aerial-imagery). The model for our deep learning is standard UNett model.
> Visit [devpost](https://devpost.com/software/solarian) for more information on the project

## 🤔 How Our Solution Works
> Users input a location via an address or using longitude/langitude values and choose the image 'patch' that best represents the building users are trying to target. The app will return information such as surface area of flat roof (for installation of solar panels) and money saved per time period after installing solar panels at specified 'patch'.

## 𝌞 Repository Content
1. [Machine Learning Model](https://github.com/enlihhhhh/MLDA-DLW-Project-Solarian/blob/main/Training.ipynb)
    - Notebook contains the various ML models we used for the training of data
    - Data contains images derived from a kaggle data-set
2. [Weather Data](https://github.com/enlihhhhh/MLDA-DLW-Project-Solarian/blob/main/Weather_Data.ipynb)
    - Notebook contains the algorithm we design to calculate the highest efficiency of solar panels
    - Data contains different weather conditions which may affect the solar radiation
3. Source Code
    - [Home Page App](https://github.com/enlihhhhh/MLDA-DLW-Project-Solarian/blob/main/app.py)
    - [Second Page App](https://github.com/enlihhhhh/MLDA-DLW-Project-Solarian/tree/main/pages)
4. [Presentation Slides](https://github.com/enlihhhhh/MLDA-DLW-Project-Solarian/blob/main/Solarian%20presentation%20slides.pdf)

## 🧑🏻‍💻 Technologies
* Frontend: 
    - StreamLit
* Backend for our Machine-Learning Model: 
    - OpenCV, Keras, TensorFlow, segmentation_models
* Other libraries used: 
    - Pandas, Patchify, Sckitlearn, Geopy, Pillow, Matplotlib

## 😰 Challenges
* Getting accuracy for the actual commerical and industrial use due to lack of data and optimisation of model
* Unable to allow users to specify exactly what buildings to be ran through the model
* Integration hell trying to integrate everything together
* Certain quality of life functionalities not implemented on time 
* Weather data is categorised into regions ('North','South','East','West','Central') of singapore currently only

## 🥇 Accomplishments
* Excellent accuracy of ~0.87 on training model using Standard UNett for image segmentation over 100 epochs
* Implemented a decent frontend UI on StreamLit given lack of time and experience
* Managed to establish a direct relationship between 'regions of Singapore' and 'money saved through installation of solar panel'

## 👀 Future Plans
* Fine-tune the model and feed more data for training the model to get extremely high accuracy for actual use
* Fully implement all front-end quality of life features such as an automatic screenshot of the map
* Expand the usage of this app outside of Singapore
* Give more accurate metrics of and conversion of pixels to the surface area
* Addition of more features in Computer Vision aspect such as calculating angle of the roof

## ✍🏻 Contributors
* Daniel Tan [@UnicornPresident](https://github.com/UnicornPresident)
* Arun Vijay [@hackermanrunzzz](https://github.com/hackermanrunzzz)
* Wang Yu Teng [@WangYuTengg](https://github.com/WangYuTengg)
* Lye En Lih [@enlihhhhh](https://github.com/enlihhhhh)

## ※ References
* https://www.photonicuniverse.com/en/resources/articles/full/7.html#:~:text=Finally%2C%20to%20calculate%20the%20maximum,100%20to%20get%20a%20percentage.
* http://solargy.com.sg/new/index.php?route=information/faq&page=2#:~:text=What%20is%20the%20annual%20irradiation,1580%20to%201620%20kWh%2F%20m2
* https://www.saurenergy.com/solar-energy-blog/here-is-how-you-can-calculate-the-annual-solar-energy-output-of-a-photovoltaic-system#:~:text=Globally%20a%20formula%20E%20%3D%20A,output%20of%20a%20photovoltaic%20system.&text=Example%20%3A%20the%20solar%20panel%20yield,of%201.6%20m%C2%B2%20is%2015.6%25%20
* https://www.ema.gov.sg/Renewable_Energy_Overview.aspx#:~:text=In%20Singapore%2C%20we%20have%20limited,when%20it%20becomes%20commercially%20viable
* https://nealanalytics.com/blog/7-steps-successful-computer-vision-poc/
* https://www.kaggle.com/datasets/humansintheloop/semantic-segmentation-of-aerial-imagery
* http://www.weather.gov.sg/climate-historical-daily/
* https://docs.mapbox.com/help/glossary/zoom-level/
* https://omdena.com/blog/machine-learning-rooftops
* https://www.saurenergy.com/solar-energy-blog/here-is-how-you-can-calculate-the-annual-solar-energy-output-of-a-photovoltaic-system#:~:text=Globally%20a%20formula%20E%20%3D%20A,output%20of%20a%20photovoltaic%20system.&text=Example%20%3A%20the%20solar%20panel%20yield,of%201.6%20m%C2%B2%20is%2015.6%25%20
