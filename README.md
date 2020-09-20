# Health Prevent Technology

## Introdução

<p>
    Repositório de uma API desenvolvida para o backend da Health Prevent Technology. O objetivo da API é facilitar a integração da tecnologia de envio de sms's e mensagens de voz que já existem em grandes operadoras de plano de saúde, mas não tem em planos pequenos e médios.
</p>

<p>
    Esta API se conecta com um banco de dados PostgreSQL onde são armazenados os dados necessários apenas para notificar os clientes da operadora através de mensagens, após terem confirmado a vontade de recebê-los.
</p>

<p>
    Para as notificações com mensagens de sms e voz foi utilizada a API do Zenvia Total Voice.
</p>

## Endpoints

<p>
    Existem dois tipos de Endpoints: para consulta de dados, com requisições do tipo <b>get</b> e envio de mensagems de texto (sms) e voz (tts), com requisições do tipo <b>post</b>.
</p>

### Consulta de dados (requisições GET)

#### **/**

<p>
    Redireciona a API para a página de documentação.
</p>
 
 #### **/clients**

<p>
    Exibe todos os clientes cadastrados pela operadora de plano de saúde para envio das mensagens.
</p>

#### **/clients/disease/{type_disease}**

<p>
    Retorna lista de clientes cadastrados pela operadora de plano de saúde, a partir do tipo de condição clínica.
</p>

#### **/clients/age/{min}/{max}**

<p>
    Retorna lista de clientes cadastrados pela operadora de plano de saúde, a partir do intervalo de idade definido.
</p>

### Envio de mensagens (requisições POST)

<p>
    O envio de mensages requer um body (JSON) que será responsável por informar sobre qual público a mensagem será enviada (por condição clínica ou idade), o nome da operadora de Plano de Saúde que está enviando e a mensagem propriamente dita. Seguindo o padrão a seguir:
</p>

```javascript
{
    eventName: string,
    minAge: integer,
    maxAge: integer,
    clinicalCOndition: string,
    message: string,
    company: string
}
```

#### **/notification/sms/disease**

<p>
    Envia mensagem de sms para os clientes da operadora de plano de saúde filtrados pela condição clínica selecionada.
</p>

#### **/notification/sms/age**

<p>
    Envia mensagem de sms para os clientes da operadora de plano de saúde filtrados pela idade.
</p>

#### **/notification/tts/disease**

<p>
    Envia mensagem de voz para os clientes da operadora de plano de saúde filtrados pela condição clínica selecionada.
</p>

#### **/notification/tts/age**

<p>
    Envia mensagem de voz para os clientes da operadora de plano de saúde filtrados pela idade.
</p>