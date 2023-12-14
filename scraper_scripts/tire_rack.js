

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
    await sleep(1000);
    return xhr;
};

const uploadVehicle = async (make, year, model, additional)=>{
    const response = await fetch('http://127.0.0.1:8000/vehicle',{
        method: 'POST',
        headers:{
            'Accept':'application/json',
            'Content-Type':'application/json'
        },
        body:JSON.stringify({
            'make':make,
            'year':year,
            'model':model,
            'additional':additional
        })

    });

    if (!response.ok) {
      console.log('upload vehicle error');
      console.log(response.status);
    }else{
        console.log('upload successfully');
    }

}
const getLatestVehicle = async ()=>{
    const response = await fetch('http://127.0.0.1:8000/vehicle/latest',{
        method: 'GET',
        headers:{
            'Accept':'application/json',
            'Content-Type':'application/json'
        },
    });

    if (!response.ok) {
        console.log('get latest vehicle error');
        console.log(response.status);
        return null;

    }else{
        return response.json();
    }

}

const runScript =async ()=>{

    // const makes = ['Porsche', 'BMW','Alfa Romeo', 'Aston Martin','Audi','Ford','Honda','Hyundai','Isuzu','Jaguar',
    // 'Jeep','Kia','Land Rover','Lexus','Maybach','Mazda','McLaren','Mercedes-Benz','Mercedes-Maybach',
    // 'MINI','Mitsubishi','Nissan','Rivian','Rolls-Royce','Saab','smart','Subaru','Suzuki','Tesla','Toyota',
    // 'Volkswagen','Volvo'];
    const makes = ['Porsche'];
    const previousVehicle = await getLatestVehicle();
    // const previousVehicle = {};

    let previousMake = previousVehicle?.make||null;
    let previousYear = previousVehicle?.year||null;
    let previousModel = previousVehicle?.model||null;
    let previousAdditional = previousVehicle?.additional||null;


    const makeIndexStart = makes.indexOf(previousMake)<0? 0 : makes.indexOf(previousMake);
    previousMake = null;

    for(var i=makeIndexStart;i<makes.length;i++){
        let make = makes[i];
        


        let xhr = await getVehicleInfo(make, '', '');


        while (xhr.readyState != 4 || xhr.status != 200) {
            // console.log(xhr.status);
            console.log(xhr.responseText);
            console.log('error get year');
            return;
            // await sleep(5000);
            // xhr = await getVehicleInfo(make, '', '');
        } 

        let year_tags = xhr.responseXML.getElementsByTagName("year");
        let years = [];

        for(var l=0;l<year_tags.length;l++){
            years.push(year_tags[l]?.childNodes?.[0]?.nodeValue);
        }
        

        const yearIndexStart = years.indexOf(previousYear?.toString())<0? 0 : years.indexOf(previousYear?.toString());
        previousYear = null;


        for(var j=yearIndexStart;j<years.length;j++){
            let year = years[j];



            let xhr = await getVehicleInfo(make, year, '');
            while (xhr.readyState != 4 || xhr.status != 200) {

                console.log(xhr.responseText);
                console.log('error get model');
                return;

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
            console.log(models);


            const modelIndexStart = models.indexOf(previousModel)<0? 0 : models.indexOf(previousModel);
            previousModel = null;

            for(var k=modelIndexStart;k<models.length;k++){
                let model = models[k];


                let xhr = await getVehicleInfo(make, year, model);
                while (xhr.readyState != 4 || xhr.status != 200) {

                    console.log('error get additional');
                    return;

                    console.log(xhr.status);
                    console.log(xhr.responseText);
                    await sleep(5000);
                    xhr = await getVehicleInfo(make, year, model);
                } 

                if( xhr.responseXML.getElementsByTagName("clar").length){
                    let clar_tags = xhr.responseXML.getElementsByTagName("clar");
                    for(var m=0;m<clar_tags.length;m++){
                        let additional = clar_tags[m]?.childNodes?.[0]?.nodeValue;
                        console.log({'make':make, 'year':year, 'model':model, 'additional':additional});
                        await uploadVehicle(make, year, model, additional);
                    }
                }else{
                    console.log({'make':make, 'year':year, 'model':model, 'additional':''});
                    await uploadVehicle(make, year, model, '');
                }

            }
        }

    }
}




while(true){
    try{
        await runScript();
    }
    catch(e){
        console.log(e)
        console.log('waiting...');
        await sleep(5*60*1000);
    }
}

// {
// additional
// : 
// "Standard Tire"
// make
// : 
// "BMW"
// model
// : 
// "M440i Gran Coupe"
// year
// : 
// "2024"}