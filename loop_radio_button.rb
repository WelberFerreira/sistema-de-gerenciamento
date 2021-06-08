      <% lista = :legibilidade, :respeito_margens, :indi_paragr, :estr_paragr %>
      <%lista.each do |l|%>
          <%= form.radio_button l, "teste"%> &nbsp
          <%= form.label l, "Excelente"%> &nbsp
        <%=l%>
        <br>
      <%end%>
