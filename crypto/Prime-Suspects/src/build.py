from pathlib import Path


P = 13183170791428551076382706417537366308741690296103920563975563247628528203949239179272907935356437685040523167590380773443662574661274253458398359053427379
Q = 12418370253593242931532006421397235974001548936438336138224060713087604932537142560347957297239106462590216666093419895637049907879062360304531808200189871
E = 65537
PLAINTEXT = (
    "RSA RECOVERY COMPLETE\n"
    "Flag: sentctf{f4ct0r5_bu1ld_th3_k3y}\n"
    "Next case: PRIME_SUSPECTS_PART_2"
)


def main():
    n = P * Q
    message = int.from_bytes(PLAINTEXT.encode(), "big")
    if message >= n:
        raise ValueError("Plaintext is too large for the RSA modulus")

    ciphertext = pow(message, E, n)
    output = (
        "RSA ARCHIVE RECORD\n\n"
        "The factors used to generate this RSA key were retained in the archive.\n\n"
        f"p = {P}\n"
        f"q = {Q}\n"
        f"e = {E}\n"
        f"c = {ciphertext}\n"
    )

    destination = Path(__file__).resolve().parents[1] / "dist" / "rsa_parameters.txt"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(output, encoding="ascii")


if __name__ == "__main__":
    main()
