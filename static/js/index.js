$( document ).ready(function() {

    $('.alert').hide();

    cep_blur = function(){
        var div = $(this).parent().parent().parent();
        if($(this).val() != ''){
            url = "/cep/" + $(this).val();
            $.post(url, function(data) {
                div.find('#rua').val(data.nome);
                div.find('#bairro').val(data.bairro);
                div.find('#cidade').val(data.cidade);
                div.find('#uf').val(data.uf);
            });
        }else{
            div.find('#rua').val('');
            div.find('#bairro').val('');
            div.find('#cidade').val('');
            div.find('#uf').val(''); 
        }
    }

    $('#cep').blur(cep_blur);

    $('#btnSalvar').click(function(){
        var usuario = {};
        usuario.nome =  $('#nome').val();
        usuario.cpf = $('#cpf').val();
        if($('#sexo-0').is(':checked')){
            usuario.sexo = 'M';
        }else{
            usuario.sexo = 'F';
        }
        usuario.telefone = $('#telefone').val();
        usuario.enderecos = []

        $('.endereco-item').each(function(){
            endereco = {}
            endereco.cep = $(this).find('#cep').val();
            endereco.numero = $(this).find('#numero').val();
            endereco.complemento = $(this).find('#complemento').val();
            if(endereco.cep != ''){
                usuario.enderecos.push(endereco);
            }
        });

        $.post('/save', {'data': JSON.stringify(usuario)}, function(data) {
            if(data.result){
                $('.alert-success').show().delay(5000).fadeOut();
                $('#btnLimpar').click();
            }else{
                $('.alert-danger').html(data.message);
                $('.alert-danger').show().delay(5000).fadeOut();
            }
        }).fail(function() {
            $('.alert-danger').html('Não foi possível salvar o usuário.');
            $('.alert-danger').show().delay(5000).fadeOut();
        })

    });

    getNumEnderecos = function(){
        for(i=0; i<256; i++){
            if($('.endereco-'+i).length == 0){
                return i-1;
            }
        }
    }

    limparEndereco = function(endereco){
        endereco.find('#cep').val('');
        endereco.find('#cep').blur(cep_blur);
        endereco.find('#cep').blur();
        endereco.find('#numero').val('');
        endereco.find('#complemento').val('');
    }

    $('#btnAddEndereco').click(function(){
        n = getNumEnderecos();
        $('.endereco-'+ n).clone().appendTo('.enderecos');
        $('.endereco-'+ n).slice(1).addClass('endereco-'+ (n+1))
        $('.endereco-'+ n).slice(1).removeClass('endereco-'+ n)
        n++;
        limparEndereco($('.endereco-'+ n));
    });

    $('#btnLimpar').click(function(){
        $('#nome').val('');
        $('#cpf').val('');
        $('#sexo-0').prop('checked', true);
        $('#telefone').val('');
        $('#cep').val('');
        $('#cep').blur();
        $('#numero').val('');
        $('#complemento').val('');
        $('.endereco-item').each(function(){
            limparEndereco($(this));
        })
        $('.endereco-item').slice(1).remove();
    });
})
