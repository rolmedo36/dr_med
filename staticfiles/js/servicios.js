const listarServicios=async() =>{
    try{
        const response=await fetch("/get_servicios");
        const data=await response.json();
        console.log(data);
        if(data.message == "Success"){
            let opciones = ``;
            opciones += "<option value=''>Seleccione servicio..</option>";
            data.servicios.forEach((servicio) => {
                opciones += `<option value='${servicio.id}'>${servicio.nombre}</option>`;
            });
            cboServicios.innerHTML=opciones;
        }else{
            alert("Servicios no encontrados...");
        }

    } catch (error){
        console.log(error);
    }
};
const listarTurno=async(turno_num) =>{
    try{
        const response=await fetch(`/get_turno/${turno_num}`);
        const data=await response.json();
        console.log(data);
        if(data.message == "Success"){
            console.log('turno liberado')
        }else{
            alert("Este turno ya fue atendido ... !!");
            window.location.replace("/turno_liberar/");
        }

    } catch (error){
        console.log(error);
    }
};
const cargaInicial=async()=>{
    await listarServicios();

    cboServicios.addEventListener("change", (event) => {
        listarDisponible(cboServicios.value, txtFecha.value);
    });
    turno_num.addEventListener("change", (event) => {
        listarTurno(turno_num.value);
    });
};

window.addEventListener("load", async () => {
    await cargaInicial();
});
