var xhr = new XMLHttpRequest();

// 設置請求方法和 URL
xhr.open("GET", "https://www.tirerack.com/survey/ValidationServlet?autoMake=BMW&autoYearsNeeded=true", true);

// 設置標頭
xhr.setRequestHeader("Accept", "application/xml, text/xml, */*; q=0.01");
xhr.setRequestHeader("Accept-Language", "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7");
xhr.setRequestHeader("Cache-Control", "no-cache");
xhr.setRequestHeader("Pragma", "no-cache");
xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");

// 設置回調函數，處理請求完成後的動作
xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
        // 請求成功，處理返回的數據
        console.log(xhr.responseText);
    }
};

// 發送請求
xhr.send();






var xhr = new XMLHttpRequest();

// 設置請求方法和 URL
xhr.open("GET", "https://www.tirerack.com/survey/ValidationServlet?autoMake=BMW&autoYear=2023", true);

// 設置標頭
xhr.setRequestHeader("Accept", "application/xml, text/xml, */*; q=0.01");
xhr.setRequestHeader("Accept-Language", "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7");
xhr.setRequestHeader("Cache-Control", "no-cache");
xhr.setRequestHeader("Pragma", "no-cache");
xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");

// 設置回調函數，處理請求完成後的動作
xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
        // 請求成功，處理返回的數據
        console.log(xhr.responseText);
    }
};

// 發送請求
xhr.send();




var xhr = new XMLHttpRequest();

// 設置請求方法和 URL
xhr.open("GET", "https://www.tirerack.com/survey/ValidationServlet?autoMake=BMW&autoYear=2020&autoModel=330I%20xDrive%20Sedan&newDesktop=true", true);

// 設置標頭
xhr.setRequestHeader("Accept", "application/xml, text/xml, */*; q=0.01");
xhr.setRequestHeader("Accept-Language", "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7");
xhr.setRequestHeader("Cache-Control", "no-cache");
xhr.setRequestHeader("Pragma", "no-cache");
xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");

// 設置回調函數，處理請求完成後的動作
xhr.onreadystatechange = function () {
    if (xhr.readyState == 4 && xhr.status == 200) {
        // 請求成功，處理返回的數據
        console.log(xhr.responseText);
    }
};

// 發送請求
xhr.send();


const sleep = ms => new Promise(r => setTimeout(r, ms));

const getVehicleInfo = async (make, year, model)=>{
    var xhr = new XMLHttpRequest();
    xhr.open("GET", `https://www.tirerack.com/survey/ValidationServlet?autoMake=${make}${year?`&autoYear=${year}`:'&autoYearsNeeded=true'}${model?`&autoModel=${model}&newDesktop=true`:''}`, false);
    xhr.setRequestHeader("Accept", "application/xml, text/xml, */*; q=0.01");
    xhr.setRequestHeader("Accept-Language", "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7");
    xhr.setRequestHeader("Cache-Control", "no-cache");
    xhr.setRequestHeader("Pragma", "no-cache");
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.send();
    await sleep(5000);
    return xhr;
};


const runScript =async ()=>{
    const makes = ['BMW'];

    for(var i=0;i<makes.length;i++){
        let make = makes[i]

        let xhr = await getVehicleInfo(make, '', '');


        while (xhr.readyState != 4 || xhr.status != 200) {
            // console.log(xhr.status);
            console.log(xhr.responseText);
            console.log('error get year')
            return
            // await sleep(5000);
            // xhr = await getVehicleInfo(make, '', '');
        } 

        let year_tags = xhr.responseXML.getElementsByTagName("year");
        let years = [];

        for(var l=0;l<year_tags.length;l++){
            years.push(year_tags[l]?.childNodes?.[0]?.nodeValue);
        }

        for(var j=0;j<years.length;j++){
            let year = years[j]



            let xhr = await getVehicleInfo(make, year, '');
            while (xhr.readyState != 4 || xhr.status != 200) {

                console.log(xhr.responseText);
                console.log('error get model')
                return

                console.log(xhr.status);
                console.log(xhr.responseText);
                await sleep(5000);
                xhr = await getVehicleInfo(make, year, '');
            } 


            let model_tags = xhr.responseXML.getElementsByTagName("model");
            let models = [];

            for(var l=0;l<model_tags.length;l++){
                models.push(model_tags[l]?.childNodes?.[0]?.nodeValue);
            }
            console.log(models)

            for(var k=0;k<models.length;k++){
                let model = models[k]


                let xhr = await getVehicleInfo(make, year, model);
                while (xhr.readyState != 4 || xhr.status != 200) {

                    console.log('error get additional')
                    return

                    console.log(xhr.status);
                    console.log(xhr.responseText);
                    await sleep(5000);
                    xhr = await getVehicleInfo(make, year, model);
                } 
                
                

                if( xhr.responseXML.getElementsByTagName("clarifiers").length){
                    let clar_tags = xhr.responseXML.getElementsByTagName("clar");
                    for(var i=0;i<clar_tags.length;i++){
                        let additional = clar_tags[i]?.childNodes?.[0]?.nodeValue;

                        console.log({'make':make, 'year':year, 'model':model, 'additional':additional});
                    }
                }else{

                    console.log({'make':make, 'year':year, 'model':model, 'additional':''});


                }

            }
            return;


        }



    }
}


await runScript()

let xhr = await getVehicleInfo('BMW', '', '');
if (xhr.readyState != 4 || xhr.status != 200) {
    console.log('error');
} 


console.log(xhr.responseXML)