import os
import pygame
import configargparse

if __name__ == "__main__":
    parser = configargparse.ArgumentParser()
    # Required elements
    parser.add_argument("--dwidth", type=int, help="Display width",
                        default=800)
    parser.add_argument("--dheight", type=int, help="Display height.",
                        default=600)
    parser.add_argument("--target_path", type=str, help="Folder to target.",
                        default=".")
    # List elements
    parser.add_argument("--folders", type=str, help="Folders", nargs="+",
                        default=["f1", "f2", "f3"])

    parser.add_argument("--filetype", type=str, help="Folders", default="jpg")

    args = parser.parse_args()

    pygame.init()

    all_images = [s for s in os.listdir(args.target_path)
                  if s.endswith("." + args.filetype)]
    i_img = 0
    n_images = len(all_images)

    display_width = args.dwidth
    display_height = args.dheight

    setDisplay = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('Image sorting program')

    clock = pygame.time.Clock()
    crashed = False
    black = (0, 0, 0)
    white = (255, 255, 255)
    keys = [pygame.K_KP0, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3,
            pygame.K_KP4, pygame.K_KP5, pygame.K_KP6, pygame.K_KP7,
            pygame.K_KP8, pygame.K_KP9]

    for f in args.folders:
        if not os.path.isdir(f):
            os.makedirs(f)

    max_elems = max(len(args.folders), len(keys))
    dict_keys = {key: value for key, value in zip(keys[:max_elems],
                                                  args.folders[:max_elems])}

    for i, val in enumerate(dict_keys.values()):
        print("{} : {}".format(i, val))

    while not crashed and i_img < n_images:
        img = pygame.image.load(args.target_path + "/" + all_images[i_img])
        position = img.get_rect()
        scale_factor = max(position.width/display_width,
                           position.height/display_height)
        img = pygame.transform.scale(img, (int(position.width/scale_factor),
                                           int(position.height/scale_factor)))
        choosen_fold = False

        while not(crashed) and not(choosen_fold):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True
                if event.type == pygame.KEYUP:
                    for key, fold in dict_keys.items():
                        # print(event.key)
                        if event.key == key:
                            choosen_fold = True
                            path1 = args.target_path + "/" + all_images[i_img]
                            path2 = (args.target_path + "/" + fold + "/"
                                     + all_images[i_img])
                            print(path1, path2)
                            os.rename(path1, path2)

            setDisplay.fill(white)
            setDisplay.blit(img, (0, 0))

            pygame.display.update()
            # clock.tick(1)

        i_img += 1

    pygame.quit()
