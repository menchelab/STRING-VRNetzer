#!Python3
import load_files
import read_string
import settings as st


def main():
    for organism in st.Organisms.all_organisms:
        if organism in [
            st.Organisms.human,
            st.Organisms.ecoli,
            st.Organisms.arabidopsis,
            st.Organisms.worm,
        ]:
            continue
        tax_id = st.Organisms.get_tax_ids(organism)
        load_files.download(tax_id, organism)
        read_string.write_VRNetz(organism, "STRING")


if __name__ == "__main__":
    main()
