// ===============================
// EduGuide AI - script.js
// ===============================


const explainBtn = document.getElementById("explainBtn");


if (explainBtn) {


    explainBtn.addEventListener("click", async function () {


        const question = document
            .getElementById("question")
            .value
            .trim();



        if (question === "") {

            alert("Please enter your question.");

            return;

        }



        explainBtn.disabled = true;


        document.getElementById("question").disabled = true;

        explainBtn.innerHTML = "🤖 EduGuide AI is Teaching...";   



        const formData = new FormData();


        formData.append(
            "question",
            question
        );


        try {


            const response = await fetch(
                "/explain",
                {

                    method: "POST",

                    body: formData

                }
            );



            const data = await response.json();



            document.getElementById("concept").innerHTML =
                data.concept || "No explanation available.";



            document.getElementById("steps").innerHTML =
                data.steps || "No steps available.";



            document.getElementById("example").innerHTML =
                data.example || "No example available.";

            
            const flowchart = document.getElementById("flowchart");

            flowchart.innerHTML = "";

            const steps = (data.flowchart || "")
            .replace(/<br>/g,"\n")
            .split("\n");

            steps.forEach((step,index)=>{

            if(step.trim()!=""){

            const box=document.createElement("div");

            box.className="flow-step";

            box.innerText=step.replace(/^\d+\.\s*/,"");

            flowchart.appendChild(box);

            if(index<steps.length-1){

            const arrow=document.createElement("div");

            arrow.className="flow-arrow";

            arrow.innerHTML="⬇";

            flowchart.appendChild(arrow);

            }

            }

            });


            document.getElementById("takeaway").innerHTML =
                data.takeaway || "No takeaway available.";



            document.getElementById("practice").innerHTML =
                data.practice || "No practice question available.";


            // Smoothly scroll to the AI explanation
            document.querySelector(".response").scrollIntoView({

                behavior: "smooth",

                block: "start"

            });



        }


        catch(error) {


            console.log(error);


            alert(
                "Something went wrong while generating explanation."
            );


        }



        explainBtn.disabled = false;

        document.getElementById("question").disabled = false;

        explainBtn.innerHTML ="🚀 Ask EduGuide AI";


        



    });



}

const checkBtn = document.getElementById("checkAnswerBtn");

if(checkBtn){

checkBtn.addEventListener("click",async()=>{

const studentAnswer=document.getElementById("studentAnswer").value;

const practice=document.getElementById("practice").innerText;

if(studentAnswer.trim()===""){

alert("Please type your answer first.");

return;

}

checkBtn.disabled=true;

checkBtn.innerHTML="🤖 Checking...";

const formData=new FormData();

formData.append(
    "question",
    question
);

const imageFile = document.getElementById("image").files[0];

if(imageFile){

    formData.append("image", imageFile);

}

formData.append("practice",practice);

formData.append("answer",studentAnswer);

const response=await fetch("/check_answer",{

method:"POST",

body:formData

});

const data=await response.json();

const feedback=document.getElementById("feedback");

feedback.style.display="block";

feedback.innerHTML=data.feedback.replace(/\n/g,"<br>");

checkBtn.disabled=false;

checkBtn.innerHTML="✅ Check My Answer";

feedback.scrollIntoView({

behavior:"smooth"

});

});

}

const imageInput = document.getElementById("image");

if(imageInput){

imageInput.addEventListener("change",function(){

const file=this.files[0];

if(file){

document.getElementById("imageName").innerHTML="📷 "+file.name+" selected";

}

});

}