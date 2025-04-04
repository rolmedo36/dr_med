
const buscarCP=async(CP) =>{
    try{
        const response=await fetch(`/codigos_postales/${CP}`);
        const data=await response.json();
        // console.log(data);
        if(data.message == "Success"){
            let opciones = ``;
            let ciudad = ``;
            let estado = ``;
            opciones += "<option value=''>Seleccione colonia..</option>";
            data.cp.forEach((codigo) => {
                estado = codigo.estado;
                ciudad = codigo.ciudad;
                opciones += `<option value='${codigo.id}'>${codigo.colonia}</option>`;
            });
            cboColonia.innerHTML=opciones;
            txtCiudad.innerHTML=ciudad;
            txtEstado.innerHTML=estado;
        }else{
            alert("Paises no encontrados...");
        }

    } catch (error){
        console.log(error);
    }
};

const cargaInicial=async()=>{
    // await buscarCP();

    id_codigo_postal.addEventListener("change", (event) => {
        // console.log(event);
        // console.log(event.target);
        // console.log(event.target.value);
        buscarCP(event.target.value);
    });
};

window.addEventListener("load", async () => {
    await cargaInicial();
});
