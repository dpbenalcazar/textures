car1 = 'D:\Datasets\TextureDataset\6_Textures\';
car2 = 'C:\Users\daniel\Desktop\chl2_texture\train\digital\';
car3 = 'C:\Users\daniel\Desktop\chl2_texture\train\';

sources = {'printed', 'screen'};

random_crop = false;
random_flip = true;
extension = '.jpg';

for s = 1 %:2
    % Carpetas y archivos
    car3a = [car3, sources{s},'\'];

    if ~exist(car3a,'dir')
        mkdir(car3a)
    end

    % Encontrar nombres de texturas
    if s == 1
        Textures_pA = dir([car1, 'printedA\', '*g']);
        Textures_pB = dir([car1, 'printedB\', '*g']);
        Textures = [Textures_pA; Textures_pB];
    else
        Textures = dir([car1, 'screen\', '*g']);
    end

    Nt = length(Textures);

    % Encontrar nombres de imágenes
    Files = dir([car2, '*']);
    Files(1:2) = [];
    Nf = length(Files);

    % Variables del laso
    se = strel('disk',2);
    ind_text = randi(Nt, Nf,1);

%     % Barra de progreso
%     dwb = 1/Nf;
%     wb = 0/Nf;
%     w_bar = waitbar(wb, sources{s});

    % Laso Principal
    parfor f = 1:Nf
    % f = randi(Nf)
        n = ind_text(f);
        ID = Files(f).name;
        ID(end-3:end)=[];

        arch1 = [Textures(n).folder, '\', Textures(n).name];
        arch2 = [car2, Files(f).name];
        arch3 = [car3a, ID, extension];

        % Leer textura
        texture = iread(arch1, 'double') - 0.5;
        [H1, W1, ~] = size(texture);

        % Leer imagen
        im2 = iread(arch2, 'double');
        [H2, W2, ~] = size(im2);

        if random_crop
            % Recorte Aleatorio
            x = randi(round(W1/3));
            y = randi(round(H1/3));
            Wx = W1-x;
            Wy = round((H1-y)*W2/H2);
            max_W = min([Wx, Wy]);
            W3 = randi([round(0.67*max_W) , max_W]);
            H3 = round(W3*H2/W2);
            rect = [x, y, W3, H3];
        else
            % Recorte mayor area
            W3 = round(W2*H1/H2);
            H3 = round(H2*W1/W2);
            if H3 < H1
                y0 = randi(H1-H3);
                rect = [1, y0, W1, H3];
            elseif W3 < W1
                x0 = randi(W1-W3);
                rect = [x0, 1, W3, H1];
            else
                disp(['Problem on ', num2str(f)]); rect = [1, 1, W1, H1];
            end
        end
    %     im4 = insertShape(texture, 'Rectangle', rect, 'LineWidth',5);

        % Recortar textura
        texture = imcrop(texture, rect);
        texture = imresize(texture, [H2, W2], 'nearest');

        % Random flip
        if random_flip
            if rand(1) < 0.5
                texture = flipdim(texture ,1);
            end
            if rand(1) < 0.5
                texture = flipdim(texture ,2);
            end
        end

        % Inyectar textura
        im3 = im2 + texture;

        % Hallar máscara de segmentación
        mask = im2(:,:,1) < 5/255 & im2(:,:,2) < 5/255 & im2(:,:,3) < 5/255;
        mask = imdilate(mask, se);
        mask = imdilate(mask, se);
        mask = imerode(mask, se);
        mask = imerode(mask, se);
        mask = ~imfill(~mask,'holes');
        mask = cat(3, mask, mask, mask);

        % Remover máscara
        im3(mask) = 0;

        % Guardar Imagen
        imwrite(im3, arch3);

    %     figure(1)
    %     idisp({im2,im3})
    %     figure(2)
    %     imshow(im4)

%         wb = wb + dwb;
%         waitbar(wb, w_bar)
    end
%     close(w_bar)

end
