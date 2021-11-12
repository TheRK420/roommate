let pdfConversion = () =>{
    console.log("shivanhs")
    element = document.getElementsByClassName('invoice-container')[0];
    // element.querySelector('.hidden').hidden = true;
    const opts = {
      margin: [5,-5,0,0]
    }
    html2pdf()
    .set(opts)
    .from(element)
    .save();
    // element.querySelector('.hidden').hidden = false;
}

const pdf = document.getElementsByClassName('print')[0].addEventListener('click', pdfConversion);
// const options = {
//     margin: 0,
//     filename: 'invoice.pdf',    //name the output file
//     image: { 
//       type: 'jpeg',     //image type
//       quality: 100
//     },
//     html2canvas: { 
//       scale: 5
//     },
//     jsPDF: { 
//       unit: 'em', 
//       format: 'letter', 
//       orientation: 'portrait'   // pdf orientation
//     }
//   }
  
//     const pdfConversion = () =>{     // class for download button
//     const element = document.getElementsByClassName('invoice-container')[0];   //id for content area
//     html2pdf().from(element).set(options).save();
//   };

//   document.getElementsByClassName('print')[0].addEventListener('click', pdfConversion);