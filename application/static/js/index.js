const video = document.getElementById('video')
const canvas = document.getElementById('canvas')
const img= document.getElementById('CapturedImg')
const snap = document.getElementById('snap')
const predictBtn= document.getElementById('predict')
const AddBtn= document.getElementById('AddButton')
const SolveBtn= document.getElementById('SolveBtn')
const errorMessageElement = document.getElementById('spanErrorMsg')
const imgForm= document.getElementById('ImgForm')
const LoginForm= document.getElementById('LoginForm')
const AddedCount= document.getElementById('AddedCount')

const constraints = {
    audio: false,
    video:{
        width:400,
        height:400
    }

}

//Access Image
async function init(){
    try{
        const stream = await navigator.mediaDevices.getUserMedia(constraints)
        handleSuccess(stream)
    }
    catch(error){
        errorMessageElement.innerHTML=`navigator.getUserMedia.error:${error.toString()}`
    }
}
//Success
function handleSuccess(stream){
    window.stream= stream;
    video.srcObject= stream;
}

// Load init
init()

//Get Image
var context = canvas.getContext('2d')
snap.addEventListener('click',function(){
    context.drawImage(video,0,0,400,400);
    img.src = canvas.toDataURL('image/jpg');
})

//Prediction 

predictBtn.addEventListener("click",function(e){
    e.preventDefault()
    console.log("adams")
    $('#result_text').text('  Predicting...');
    console.log("james")
    $.ajax({
        type: "POST",
        url: "https://doaa-joshbrod-webserver-ca2/predict",
        data: img.src
    }).done(function(data){
            console.log('john')
            console.log(data)
            Probability
            $('#Probability').text((data.Probability+'%'))
            $('#result_text').text(data.prediction)
    })
            

    

});


AddBtn.addEventListener("click",function(e){
    e.preventDefault()
    if (document.getElementById('result_text').innerHTML=="" ||document.getElementById('result_text').innerHTML=="Make Prediction"
    || document.getElementById('result_text').innerHTML=='  Predicting...' ){
        $('#result_text').text("Make Prediction")
    }
    else{
        $('#AddedCount').text(parseInt(AddedCount.innerHTML)+1)
        var current_Equation=document.getElementById('EquationText').innerHTML
        console.log(current_Equation)
        if (current_Equation==NaN){    
            var new_Equation=document.getElementById('result_text').innerHTML
        }
        else{
            var new_Equation=current_Equation+document.getElementById('result_text').innerHTML
        }
        $('#Probability').text("")
        $('#result_text').text("")
        $('#EquationText').text(new_Equation);  
    }
});

SolveBtn.addEventListener("click",function(e){
    e.preventDefault()
    NumberToAdd=parseInt(AddedCount.innerHTML)
    if(NumberToAdd==0){
        $('#EquationText').text("");  
    }
    else{
        Equation= document.getElementById('EquationText').innerHTML
        console.log(Equation)
        $.ajax({
            type: "POST",
            contentType: "application/json;",
            url: "http://127.0.0.1:5000/SolveEquation",
            data: JSON.stringify({
                NumberToAdd:NumberToAdd,
                Equation: Equation
            })
        }).done(function(data){
            console.log('Louis')
            $('#Answer').text(Equation+'='+data)
            $('#AddedCount').text(0) //Prevent Any override
            $('#EquationText').text("") 
        }).fail(function() {
            $('#Answer').text('Invalid Equation')
            $('#AddedCount').text(0) //Prevent Any override
            $('#EquationText').text("") 
        })
    }
});

