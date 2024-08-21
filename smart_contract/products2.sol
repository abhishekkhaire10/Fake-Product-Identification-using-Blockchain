// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

contract Product {

    uint[] product_id;
    string[] product_name;
    uint[] product_status;
    uint[] seller_id;
    string[] shop_name;
    // mapping(bytes32 => bool) public vProducts;

    function setProduct(uint productId, string memory productName,
    uint sellerId, string memory shopName) public{

        product_id.push(productId);
        product_name.push(productName);
        product_status.push(2);  
        seller_id.push(sellerId);
        shop_name.push(shopName);
    }


    function viewAllProducts () public view returns(uint[] memory, string[] memory, uint[] memory,
    uint[] memory,  string[] memory) {

        return(product_id, product_name, product_status, seller_id, shop_name);
    }


    function viewSellerProducts (uint sellerId) public view returns(uint[] memory, string[] memory, uint[] memory){
        uint [] memory p_id = new uint[](seller_id.length);
        string [] memory seller_product = new string[](seller_id.length);
        uint[] memory p_status = new uint[](seller_id.length) ;

        if(seller_id.length > 0) {

            for(uint i = 0; i < seller_id.length; i++){
                if(seller_id[i] == sellerId){
                    p_id[i] = product_id[i];
                    seller_product[i] = product_name[i];
                    p_status[i] = product_status[i];
                }
                else{

                seller_product[i] = "0";
            }
        }
    }
        return (p_id, seller_product, p_status);
}
        


    function sellProduct (uint sProductId) public {

        uint status;
        uint i;
        uint product_index = 0;

        if(product_id.length > 0) {

            for(i = 0; i < product_id.length; i++) {

                if(product_id[i] == sProductId) {
                    product_index = i;
                }
            }
        }

        status = product_status[product_index];

        if(status == 2) {
            product_status[product_index] = 1;
        }

        if(status == 1) {
            product_status[product_index] = 0;
        }
    }




    function verifyFakeness(uint vProductId) public view returns(string memory, uint, uint, string memory, string memory) {

        bool isPresent = false;
        uint i;
        uint product_index = 0;

        if(product_id.length > 0) {

            for(i = 0; i < product_id.length; i++) {

                if(product_id[i] == vProductId){

                    product_index = i;

                    isPresent = true;
                }
            }
        }

        if(isPresent == true) {

                if(product_status[product_index] == 1){
                    // product_status[product_index] = 0; 
                     return(product_name[product_index], product_status[product_index], 
                     seller_id[product_index], shop_name[product_index], "Authentic");
                }

                else {

                    return ("Fake", 0, 0, "0", "0");
                }

                    
        } 
        else {
                return ("Invalid", 0, 0, "0", "0");
        }

    }
}

