## Homework 1

### Name:
    Thejaswini Reddy Vootkuri

### Ip Address
    159.203.189.42

### Phpmyadmin Link
    http://159.203.189.42/phpmyadmin

## Table Create statements

#### gift_options.sql

```sql
CREATE TABLE `gift_options` (
 `allowGiftWrap` tinyint(1) NOT NULL,
 `allowGiftMessage` tinyint(1) NOT NULL,
 `allowGiftReceipt` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

#### image_entities.sql

```sql
CREATE TABLE `image_entities` (
 `thumbnailImage` varchar(64) NOT NULL,
 `mediumImage` varchar(64) NOT NULL,
 `largeImage` varchar(64) NOT NULL,
 `entityType` varchar(128) NOT NULL,
 PRIMARY KEY (`thumbnailImage`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1


```

#### market_place_price.sql

```sql
CREATE TABLE `market_place_price` (
 `price` float(4,2) NOT NULL,
 `sellerInfo` tinytext NOT NULL,
 `standardShipRate` int(8) NOT NULL,
 `twoThreeDayShippingRate` float(4,2) NOT NULL,
 `availableOnline` tinyint(1) NOT NULL,
 `clearance` tinyint(1) NOT NULL,
 `offerType` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1


```

#### products.sql

```sql
CREATE TABLE `products` (
 `itemId` int(32) NOT NULL,
 `parentItemId` int(32) NOT NULL,
 `name` varchar(64) NOT NULL,
 `salePrice` float(6,2) NOT NULL,
 `upc` int(64) NOT NULL,
 `categoryPath` varchar(64) NOT NULL,
 `shortDescription` varchar(128) NOT NULL,
 `longDescription` varchar(128) NOT NULL,
 `brandName` varchar(32) NOT NULL,
 `thumbnailImage` varchar(64) NOT NULL,
 `mediumImage` varchar(64) NOT NULL,
 `largeImage` varchar(64) NOT NULL,
 `productTrackingUrl` varchar(128) NOT NULL,
 `modelNumber` varchar(32) NOT NULL,
 `productUrl` varchar(128) NOT NULL,
 `categoryNode` varchar(32) NOT NULL,
 `stock` tinytext NOT NULL,
 `addToCartUrl` varchar(128) NOT NULL,
 `affiliateAddToCartUrl` varchar(128) NOT NULL,
 `offerType` varchar(16) NOT NULL,
 `msrp` float(6,2) NOT NULL,
 `standardShipRate` float(6,2) NOT NULL,
 `color` tinytext NOT NULL,
 `customerRating` float(4,3) NOT NULL,
 `numReviews` int(8) NOT NULL,
 `customerRatingImage` varchar(32) NOT NULL,
 `maxItemsInOrder` int(8) NOT NULL,
 `size` varchar(8) NOT NULL,
 `sellerInfo` tinytext NOT NULL,
 `age` varchar(16) NOT NULL,
 `gender` tinytext NOT NULL,
 `isbn` int(32) NOT NULL,
 `preOrderShipsOn` varchar(32) NOT NULL,
 PRIMARY KEY (`itemId`,`parentItemId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```
