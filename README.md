# Solarian 
<hr style="border:2px solid gray"> 

![Saulės_elektrinė](https://user-images.githubusercontent.com/101797615/193462573-1104331e-721b-4206-b1e0-87973e132be2.jpeg)

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

## 🤔 How Our Solution Works
> Users input a location via an address or using longitude/langitude values and choose the image 'patch' that best represents the building users are trying to target. The app will return information such as surface area of flat roof (for installation of solar panels) and money saved per time period after installing solar panels at specified 'patch'.

## 𝌞 Repository Content
1. [Machine Learning Model](https://github.com/enlihhhhh/MLDA-DLW-Project-Solarian/blob/main/Training.ipynb)
    - Notebook contains the various ML models we used for the training of data
    - UNET
2. [Weather Data]
    - Notebook contains the algorithm we design to calculate the highest efficiency of solar panels
    - Data contains different weather conditions which may affect the solar radiation

## 🧑🏻‍💻 Technologies
* Frontend: StreamLit
* Backend for our Machine-Learning Model: OpenCV, Keras, TensorFlow, segmentation_models
* Other libraries used: pandas, patchify, sckitlearn, geopy, pillow, matplotlib

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
* Fine tune the model and feed more data for training the model to get extremely high accuracy for actual use
* Fully implement all front-end quality of life features such as automatic-screenshot of map
* Expand the usage of this app to outside of singapore
* Give more accurate metrics of and conversion of pixels to surface area
* Addition of more features in Computer Vision aspect such as calculating angle of roof 

## ✍🏻 Contributors
* Daniel Tan
* Arun Vijay
* Wang Yu Teng [@WangYuTengg](https://github.com/WangYuTengg)
* Lye En Lih [@enlihhhhh](https://github.com/enlihhhhh)
