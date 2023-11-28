import pandas as pd

brands = pd.read_csv("brands.csv") 
finance = pd.read_csv("finance.csv")
info = pd.read_csv("info.csv")
reviews = pd.read_csv("reviews.csv")

#merging the dataframes together
merged = brands.merge(info, on='product_id', how='outer')
merged= merged.merge(finance, on='product_id', how='outer')
merged= merged.merge(reviews, on='product_id', how='outer')
merged.dropna(inplace=True)

#finding the revenue and volume of sales for each brand
merged['price_label']= pd.qcut(merged['listing_price'],q=4, labels=['Budget','Average','Expensive','Elite'])

adidas_vs_nike= merged.groupby(['brand','price_label'],as_index=False).agg(mean_revenue=('revenue','mean'),num_products=('price_label','count')).round(2)

#grouping the description and making a dataframe to find relations with ratings and reviews
merged['desc_len']=merged['description'].str.len()
desc_len_upper=merged['desc_len'].max()
labels=['100 words','200 words','300 words','400 words','500 words','600 words','700 words']
bins=[0,100,200,300,400,500,600,700]
merged['description_label']=pd.cut(merged['desc_len'],bins=bins,labels=labels)
description_length= merged.groupby('description_label',as_index=False).agg(mean_rating=('rating','mean'),num_reviews=('reviews','count')).round(2)

#volume and median for different groups of products
footwear=merged[merged['description'].str.contains('shoe*|trainer*|foot*')]
clothing=merged[~merged.isin(footwear['product_id'])]
clothing.dropna(inplace=True)

product_types = pd.DataFrame({"num_clothing_products": len(clothing), 
                              "median_clothing_revenue":             clothing["revenue"].median(), 
                              "num_footwear_products": len(footwear), 
                              "median_footwear_revenue": footwear["revenue"].median()}, 
                              index=[0])
product_types