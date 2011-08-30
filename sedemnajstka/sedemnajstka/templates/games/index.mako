<%inherit file="/base.mako" />
<h3>${c.title}</h3>
<div class="yello" id="games">
    <p>
        <a href="/games/guess-avatar">
            <img src="/images/guess-avatar.png" width="64" height="54" /><br />
            Ugani Avatar
        </a>
    </p>
    <table id="players">
        <thead>
            <tr>
                <th>Ime</th>
                <th>Igral</th>
                <th>Uganil</th>
                <th>Zajebal</th>
                <th>%Uspeh</th>
            </tr>
        </thead>
        <tbody>
            % for player in c.players:
            <tr>
                <td>${h.link_to(player.nick_name, url('user', id=player.id), class_='elita')}</td>
                <td>${player.count_1}&times;</td>
                <td>${player.sum_1}&times;</td>
                <td>${player.count_1 - player.sum_1}&times;</td>
                <td>${int((player.sum_1 / float(player.count_1) * 100))}%</td>
            </tr>
            % endfor
        </tbody>
    </table>
</div>
